
import base64, os

import fitz
import shutil

import PyPDF2
# import PythonMagick

from PIL import Image
import math

class Utils():
    @staticmethod
    def base64encode_image(filepath):
        if not os.path.exists(filepath):
            return None
        base64_data = None
        with open(filepath,"rb") as f:
            base64_data = base64.b64encode(f.read())
        if base64_data is None:
            return None
        else:
            return base64_data.decode('utf-8')

    @staticmethod        
    def empty_folder(folderfullpath):
        """Empty content from a folder.

        if the content is a file, remove the file
        if the content is a folder, remove the folder totally

        Args:
            folderfullpath: the path we want to empty.

        Returns:
            None

        Raises:
            IOError: An error occurred accessing the bigtable.Table object.
        """
        if(os.path.isdir(folderfullpath)):
            for file_ in os.listdir(folderfullpath):
                fp = os.path.join(folderfullpath, file_)
                if os.path.isfile(fp):
                    os.remove(fp)
                elif os.path.isdir(fp):
                    shutil.rmtree(fp)

    @staticmethod
    def pdf2image(sourcefile, img_target_folder, shrink_times=4.0, pages=None):
        if not os.path.exists(sourcefile):
            print('File[{}] not exists! Please double check!'.format(sourcefile))
            return 
        if not os.path.exists(img_target_folder) or not os.path.isdir(img_target_folder):            
            if not os.path.exists(img_target_folder):
                # os.mkdir(img_target_folder, 777)
                os.makedirs(img_target_folder, exist_ok=True)
            else:
                print('Folder[{}] is not a folder, Please double check'.format(img_target_folder))
                return 
                
        Utils.empty_folder(img_target_folder)
        doc = fitz.open(sourcefile)
        print(doc.pageCount)
        page_list = [x for x in range(doc.pageCount)]
        if pages is not None: page_list = list(set([x if x>=0 else doc.pageCount+x for x in pages]))
        # filename = Utils.get_file_name(sourcefile)
        # img_target_folder = os.path.join(targetfolder, filename)
        # for pg in range(doc.pageCount):
        for pg in page_list:
            page = doc[pg]
            rotate = int(0)
            # every shrink parameters is 2, it will generate 4 times more clear image in pixel
            zoom_x = shrink_times
            zoom_y = shrink_times
            trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
            pm = page.getPixmap(matrix=trans, alpha=False)
            targetfilepath = os.path.join(img_target_folder, '{}.png'.format(pg))
            pm.writePNG(targetfilepath)

    @staticmethod
    def crop_image(imagefile, output_folder, col_num=1, direction='vertical'):
        im = Image.open(imagefile)
        img_size = im.size
        print('image size:{}'.format(img_size))  
        size_limit = 4096
        start_x = 0
        start_y = 0
        img_width = img_size[0]-start_x
        img_height = img_size[1] - start_y

        # clean the folder
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)
        os.mkdir(output_folder, 777)

        w = int(min(math.ceil(img_width/col_num), size_limit))
        h = min(img_height, size_limit)

        horizontal_num = math.ceil(img_width/w)
        vertical_num = math.ceil(img_height/h)

        count = 0
        if direction.lower() == 'vertical':
            for j in range(horizontal_num):
                for i in range(vertical_num):
                    x,y=start_x, start_y
                    x = x + w*j
                    y = y + h*i
                    region = im.crop((x,y, x+w, y+h))
                    count = count+1
                    output_file = os.path.join( output_folder, '{}_{}.png'.format('crop_average', str(count)) )
                    region.save(output_file)
        else:
            for j in range(vertical_num):
                for i in range(horizontal_num):
                    x,y=start_x, start_y
                    x = x + w*j
                    y = y + h*i
                    region = im.crop((x,y, x+w, y+h))
                    count = count+1
                    output_file = os.path.join( output_folder, '{}_{}.png'.format('crop_average', str(count)) )
                    region.save(output_file)

            

    # @staticmethod
    # def pdf2image_withinsize(sourcefile, img_target_folder, size):
    #     if not os.path.exists(sourcefile):
    #         print('File[{}] not exists! Please double check!'.format(sourcefile))
    #         return 
    #     if not os.path.exists(img_target_folder) or not os.path.isdir(img_target_folder):            
    #         if not os.path.exists(img_target_folder):
    #             os.mkdir(img_target_folder, 777)
    #         else:
    #             print('Folder[{}] is not a folder, Please double check'.format(img_target_folder))
    #             return 

    #     Utils.empty_folder(img_target_folder)
    #     pages = 0
    #     with open(sourcefile, 'rb') as f:
    #         pages = PyPDF2.PdfFileReader(f).getNumPages()
    #     try:
    #         for i in range(pages):
    #             image = PythonMagick.Image()
    #             # image.density(str(size))
    #             # image.resize(str(size))
    #             image.read('{}[{}]'.format(sourcefile, str(i)))
    #             image.magick('PNG')
    #             targetfilepath = os.path.join(img_target_folder, '{}.png'.format(i))
    #             image.write(targetfilepath)
    #     except Exception as ex:
    #         print(ex)


    
