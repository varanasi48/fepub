from xml.etree.ElementTree import Element, SubElement, ElementTree

def generate_nav_xhtml(output_path, nav_items):
    # Create the root element for the nav.xhtml file
    html = Element('html', {
        'xmlns': 'http://www.w3.org/1999/xhtml',
        'xmlns:epub': 'http://www.idpf.org/2007/ops'
    })

    # Add head section
    head = SubElement(html, 'head')
    SubElement(head, 'title').text = 'Table of Contents'
    SubElement(head, 'meta', {'charset': 'UTF-8'})  # Added meta charset

    # Add body section
    body = SubElement(html, 'body')
    nav = SubElement(body, 'nav', {'epub:type': 'toc', 'id': 'toc'})
    SubElement(nav, 'h1').text = 'Table of Contents'

    # Add list of navigation items
    ol = SubElement(nav, 'ol')
    for item in nav_items:
        li = SubElement(ol, 'li')
        a = SubElement(li, 'a', {'href': item['href']})
        a.text = item['title']

    # Write to file
    tree = ElementTree(html)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)

# Example usage
nav_items = [
    {'title': 'Chapter 1', 'href': 'html/page1/page1.xhtml'},
    {'title': 'Chapter 2', 'href': 'html/page2/page2.xhtml'},
    # Add more chapters as needed
]

output_path = 'd:\\newmistral\\nav.xhtml'  # Updated to absolute path
generate_nav_xhtml(output_path, nav_items)