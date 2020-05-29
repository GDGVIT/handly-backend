import argparse
from docx import Document
from PIL import Image
import joblib

from .page_parser import PageParser

class DocumentParser(PageParser):
    def __init__(self, hashes, CHARS_PER_LINE, LINES_PER_PAGE): 
        PageParser.__init__(self, hashes, CHARS_PER_LINE)
        self.LINES_PER_PAGE = LINES_PER_PAGE
    

    def parse_document(self, document, destination_path):
        pageImages = self.parse_pages_constrained(document, self.LINES_PER_PAGE, False)

        # Each image (currently an np.ndarray) has to be converted into a PIL Image
        # these images are stored in allImages:
        allImages = []
        for index in range(1, len(pageImages)):
            allImages.append(
                Image.fromarray(pageImages[index].astype('uint8'), 'RGB')
            )
        firstPage = Image.fromarray(pageImages[0].astype('uint8'), 'RGB')
        firstPage.save(destination_path, "PDF", save_all = True, append_images = allImages, resolution = 100.0)

def main(input_loc,output,pickle_loc):
    # output = '/Users/unknown-guy-1610/Desktop/Projects/Handly/twertest.pdf'
    # input_loc = '/Users/unknown-guy-1610/Desktop/Projects/Handly/test.docx'
    # pickle_loc = '/Users/unknown-guy-1610/Desktop/Projects/Handly-App/Algo/hashes.pickle'
    document = Document(input_loc)
    HASHES_PATH = pickle_loc
    CHARS_PER_LINE = 54
    LINES_PER_PAGE = 30
    with open(HASHES_PATH, 'rb') as f:
        hashes = joblib.load(f)
    document_parser = DocumentParser(hashes, CHARS_PER_LINE, LINES_PER_PAGE)
    try: 
        document_parser.parse_document(document,output)
        return True,output
    except KeyError as e:
        print("error :",str(e)[1])
        return False,str(e)[1]

if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Output pages for docx document')
    # parser.add_argument('document_path', type=str, nargs = 1)
    # parser.add_argument('out_path', type = str, nargs = 1)
    # args = parser.parse_args()

    main('','','')