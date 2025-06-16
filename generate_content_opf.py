import os
from xml.etree.ElementTree import Element, SubElement, ElementTree

def generate_content_opf(output_path, metadata, base_dir):
    package = Element('package', {
        'xmlns': 'http://www.idpf.org/2007/opf',
        'version': '3.0',
        'xml:lang': 'en',
        'unique-identifier': metadata['identifier'],
        'prefix': 'rendition: http://www.idpf.org/vocab/rendition/#'
    })

    # Metadata
    metadata_elem = SubElement(package, 'metadata', {
        'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
        'xmlns:opf': 'http://www.idpf.org/2007/opf'
    })
    for key, value in metadata.items():
        SubElement(metadata_elem, f'dc:{key}').text = value

    # Manifest
    manifest = SubElement(package, 'manifest')

    # Add navigation document for EPUB 3.0
    nav_item = SubElement(manifest, 'item', {
        'id': 'nav',
        'href': 'nav.xhtml',
        'media-type': 'application/xhtml+xml',
        'properties': 'nav'
    })

    spine = SubElement(package, 'spine')  # Removed toc="ncx"

    # Automatically detect files
    for root, _, files in os.walk(base_dir):
        for file in files:
            # Construct the file path to match the desired structure
            relative_dir = os.path.relpath(root, base_dir)
            file_path = os.path.join('html', relative_dir, file)  # Ensure 'html' is part of the path
            file_id = os.path.splitext(file)[0].replace('.', '_').replace('-', '_')
            media_type = get_media_type(file)

            # Ensure the file path matches the expected structure
            file_path = file_path.replace('\\', '/')

            SubElement(manifest, 'item', {
                'id': file_id,
                'href': file_path,  # Use the corrected file path
                'media-type': media_type
            })

            # Add XHTML files to spine
            if media_type == 'application/xhtml+xml':
                SubElement(spine, 'itemref', {'idref': file_id})

    # Ensure the manifest includes a reference to the NCX file (optional for backward compatibility)
    ncx_item = SubElement(manifest, 'item', {
        'id': 'ncx',
        'href': 'toc.ncx',
        'media-type': 'application/x-dtbncx+xml'
    })

    # Guide (optional)
    guide = SubElement(package, 'guide')

    # Write to file
    tree = ElementTree(package)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)

def get_media_type(file_name):
    ext = os.path.splitext(file_name)[1].lower()
    return {
        '.html': 'application/xhtml+xml',
        '.xhtml': 'application/xhtml+xml',
        '.css': 'text/css',
        '.otf': 'application/vnd.ms-opentype',
        '.ttf': 'application/vnd.ms-opentype',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.mp3': 'audio/mpeg',
        '.smil': 'application/smil+xml'
    }.get(ext, 'application/octet-stream')

# Example usage
metadata = {
    'title': 'How Rabbit Lost His Tail',
    'identifier': 'epub978-1-60859-632-4',
    'language': 'en-US',
    'creator': 'retold by Cynthia Swain',
    'publisher': 'Benchmark Education Company',
    'rights': '© 2009 Benchmark Education Company, LLC.'
}

# Use relative paths for base_dir and output_path
base_dir = os.path.join('.', 'html')  # Ensure this points to the directory with XHTML files
output_path = os.path.join('.', 'content.opf')

generate_content_opf(output_path, metadata, base_dir)