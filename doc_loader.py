# import unstructed document loader from langchain_community.document_loaders
from langchain_community.document_loaders import (
    PDFPlumberLoader,
    TextLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredPowerPointLoader,
    UnstructuredExcelLoader,
    CSVLoader,
    UnstructuredMarkdownLoader,
    UnstructuredXMLLoader,
    UnstructuredHTMLLoader,
)
import os



def load_document(file_path):
    """
    extrac plain text from various unstructured document
    
    :param file_path: doc file
    :return: the plain text of the document
    """

    # define the diction of document loader, will auto choose the parameter and loader class according to the doc type
    DOCUMENT_LOADER_MAPPING = {
        ".pdf": (PDFPlumberLoader, {}),
        ".txt": (TextLoader, {"encoding": "utf8"}),
        ".doc": (UnstructuredWordDocumentLoader, {}),
        ".docx": (UnstructuredWordDocumentLoader, {}),
        ".ppt": (UnstructuredPowerPointLoader, {}),
        ".pptx": (UnstructuredPowerPointLoader, {}),
        ".xlsx": (UnstructuredExcelLoader, {}),
        ".csv": (CSVLoader, {}),
        ".md": (UnstructuredMarkdownLoader, {}),
        ".xml": (UnstructuredXMLLoader, {}),
        ".html": (UnstructuredHTMLLoader, {}),
    }

    # get the file extension
    ext = os.path.splitext(file_path)[1]  
    # get the doc loader class and class parameter according to the extension
    loader_tuple = DOCUMENT_LOADER_MAPPING.get(ext)  

    # check if the doc extension is supported
    if loader_tuple: 
        loader_class, loader_args = loader_tuple  
        # instance the doc loader class
        loader = loader_class(file_path, **loader_args)  
        # loading the document
        documents = loader.load()  
        # join all the page content with \n
        content = "\n".join([doc.page_content for doc in documents])  
        # print(f"head 100 characters of document: {file_path} is: {content[:100]}...")  
        return content  

    print(file_path+f"，Unsupported doc type: '{ext}'")
    return ""




def save_uploaded_file(uploaded_file, path):
    """
    save uploaded file into server cache path
    
    :param        uploaded_file: uploaded file object from webui
    :param        path:          where the uploaded file located on server
    :return:      the full path of uploaded file on server
    """
    file_bytes = uploaded_file.read()
    full_path = os.path.join(path, uploaded_file.name)
    with open(full_path, "wb") as f:
        f.write(file_bytes)
    return full_path