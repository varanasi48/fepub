import json
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree

def generate_toc_ncx(special_pages_json_path, text_coords_dir, output_path):
    # Load special pages information
    with open(special_pages_json_path, 'r', encoding='utf-8') as f:
        special_pages = json.load(f)

    # Create the root element for the NCX file
    ncx = Element('ncx', {
        'xmlns': 'http://www.daisy.org/z3986/2005/ncx/',
        'version': '2005-1'
    })

    # Add head section
    head = SubElement(ncx, 'head')
    SubElement(head, 'meta', {'name': 'dtb:uid', 'content': 'epub978-1-60859-632-4'})
    SubElement(head, 'meta', {'name': 'dtb:depth', 'content': '1'})
    SubElement(head, 'meta', {'name': 'dtb:totalPageCount', 'content': '0'})
    SubElement(head, 'meta', {'name': 'dtb:maxPageNumber', 'content': '0'})

    # Add docTitle
    doc_title = SubElement(ncx, 'docTitle')
    SubElement(doc_title, 'text').text = 'How Rabbit Lost His Tail'

    # Add navMap
    nav_map = SubElement(ncx, 'navMap')

    # Add special pages to navMap
    play_order = 1
    for page in special_pages:
        if isinstance(page, dict) and 'title' in page and 'file' in page:
            nav_point = SubElement(nav_map, 'navPoint', {
                'id': f'navPoint-{play_order}',
                'playOrder': str(play_order)
            })
            nav_label = SubElement(nav_point, 'navLabel')
            SubElement(nav_label, 'text').text = page['title']
            SubElement(nav_point, 'content', {'src': f"html/{page['file']}"})
            play_order += 1

    # Add regular pages based on text coordinates
    for coords_file in Path(text_coords_dir).glob('*_coords.json'):
        base_name = coords_file.stem.split('_')[0]
        nav_point = SubElement(nav_map, 'navPoint', {
            'id': f'navPoint-{play_order}',
            'playOrder': str(play_order)
        })
        nav_label = SubElement(nav_point, 'navLabel')
        SubElement(nav_label, 'text').text = f"Page {base_name}"
        SubElement(nav_point, 'content', {'src': f"html/{base_name}/{base_name}.xhtml"})  # Updated path
        play_order += 1

    # Write the NCX file
    tree = ElementTree(ncx)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)

# Example usage
special_pages_json_path = Path('special_pages_selection.json')
text_coords_dir = Path('text_coords')
output_path = Path('toc.ncx')

generate_toc_ncx(special_pages_json_path, text_coords_dir, output_path)