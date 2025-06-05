from htmlnode import HTMLNode
from textnode import TextType, TextNode, text_node_to_html_node  
import re

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes



def split_nodes_delimiter(old_nodes, delimiter, text_type): 
    """
    Splits nodes based on a delimiter and returns a list of new nodes.
    
    Args:
        old_nodes (list): List of nodes to split.
        delimiter (str): The delimiter to split the text by.
        text_type (TextType): The type of text for the new nodes.
        
    Returns:
        list: A list of new nodes created from the split text.
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        #if not node.tag or not node.value:
        #    continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        #if len(sections) % 2 == 0:
        #    raise ValueError("Invalid HTML: even number of sections")
        for i in range(0, len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:  
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
            split_nodes.append(split_nodes)       
        new_nodes.extend(split_nodes if split_nodes else [])
    return new_nodes

def extract_markdown_images(text):
    """
    Extracts markdown images from the text and returns a list of TextNode objects.
    
    Args:
        text (str): The input text containing markdown images.
        
    Returns:
        list: A list of TextNode objects representing the extracted images.
    """
    
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    return [TextNode(alt_text, TextType.IMAGE, url) for alt_text, url in matches]

def extract_markdown_links(text):
    """
    Extracts markdown links from the text and returns a list of TextNode objects.
    
    Args:
        text (str): The input text containing markdown links.
        
    Returns:
        list: A list of TextNode objects representing the extracted links.
    """
    
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    return [TextNode(alt_text, TextType.LINK, url) for alt_text, url in matches] 

def split_nodes_image(old_nodes):   
    """
    Splits nodes based on markdown image syntax and returns a list of new nodes.
    
    Args:
        old_nodes (list): List of nodes to split.
        
    Returns:
        list: A list of new nodes created from the split text.
    """
    return split_nodes_delimiter(old_nodes, "![", TextType.IMAGE)

def split_nodes_link(old_nodes):
    """
    Splits nodes based on markdown link syntax and returns a list of new nodes.
    
    Args:
        old_nodes (list): List of nodes to split.
        
    Returns:
        list: A list of new nodes created from the split text.
    """
    return split_nodes_delimiter(old_nodes, "[", TextType.LINK) 


if __name__ == "__main__":
    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_link([node])
    for node in new_nodes:
        print(node)
    print("*****Starting Text_to TextNodes*****")
    text = "This is "
    #print(text_to_textnodes(text))
    #print(text_to_textnodes("This is a test text"))
    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)  " 
    nodes = (text_to_textnodes(text))
    for node in nodes:

        print(f"NODE: {node}\n") 

