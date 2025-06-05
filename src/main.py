from textnode import TextNode, TextType
import os
import shutil
from markdown_blocks import markdown_to_html_node   
import htmlnode 
import sys

def generate_page(from_path, template_path, dest_path):
    """
    Generates a page from a markdown file using a template.
    """
    if not os.path.exists(from_path):
        raise FileNotFoundError(f"Markdown file {from_path} does not exist.")
    
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file {template_path} does not exist.")
    
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    node = markdown_to_html_node(markdown_content)
    #print(f"Node : {node}")
    html = node.to_html()
    #print(f"HTML content: {html[:100]}...")  # Print first 100 characters for brevity   
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    #template_content.to_html(html) 
    
    title = extract_title(markdown_content)
    #template_content = template_content.replace("{{ Title }}", title)
    #page_content = template_content.replace("{{ Content }}", html) 
    

    # Replace placeholders in the template
    page_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html)
    page_content= page_content.replace('href=/"', 'href="{basepath}').replace('src=/"', 'src="{basepath}') 
    
    #print(f"Page content length: {len(page_content)} characters")
    #print(f"Title extracted: {title}")
    #print(f"Markdown content length: {len(markdown_content)} characters")
    #print(f"Template content length: {len(template_content)} characters")   
    #print(f"Template path: {template_path}")
    #print(f"Markdown path: {from_path}")    
    #print(f"Destination path: {dest_path}") 


    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(page_content)

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")  
    print(f"Page generated at {dest_path}")

    return


def generate_pages_recursive(content_dir, template_path, dest_dir):
    """
    Recursively generates HTML pages from markdown files in the content directory.
    """
    if not os.path.exists(content_dir):
        raise FileNotFoundError(f"Content directory {content_dir} does not exist.")
    
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file {template_path} does not exist.")
    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if file.endswith('.md'):
                from_path = os.path.join(root, file)
                relative_path = os.path.relpath(from_path, content_dir)
                dest_path = os.path.join(dest_dir, relative_path.replace('.md', '.html'))
                dest_folder = os.path.dirname(dest_path)
                
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)
                
                generate_page(from_path, template_path, dest_path)
    
    print(f"All pages generated in {dest_dir}")

    return

def extract_title(markdown):        
    
    lines = markdown.splitlines()
    if not lines:
        return ""
    
    h1line = ""
    for line in lines:
        if line.startswith("# "):
            h1line = line[2:].strip()
    if not h1line:
        raise ValueError(f"Markdown title should be a single line starting with '# ' but found: {h1line}")
    
    return h1line
         

def copy_files_recursive(source_dir_path, dest_dir_path):

    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        #print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)
    return 
  

def main():

    sys.argv = ["/"]
    #print("This is a test of the textnode module.")
    node = TextNode("This is some anchor text", TextType.LINK, "https://boot.dev")
    #print(node)
    assert node.text == "This is some anchor text"
    assert node.text_type == TextType.LINK
    assert node.url == "https://boot.dev"
    #print("Test passed!")

    #print("Deleting public directory...")
    dir_path_static = "./static"
    dir_path_public = "./public"
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    #print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    #dir_path_content = "./content"
    #if not os.path.exists(dir_path_content):
    #    raise FileNotFoundError(f"Content directory {dir_path_content} does not exist.")        
    #copy_files_recursive(dir_path_content, dir_path_public) 
    
    from_path = "./content/index.md"
    template_path = "./template.html"
    dest_path = "./public/index.html"
    #generate_page(from_path, template_path, dest_path)

    generate_pages_recursive("./content", "./template.html", "./public")    

if __name__ == "__main__":
    main()
    