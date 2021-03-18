import unittest, os
import utils

class TestUtils(unittest.TestCase):
    def test_pdf2img(self):
        input_pdf = r"C:\Users\songm28\Pfizer\Downloads\artwork125.pdf"
        output_img_folder = os.path.basename(input_pdf).split(".")[0].replace(" ", "_")
        utils.Utils.pdf2image(sourcefile=input_pdf, img_target_folder=output_img_folder, pages=[0,-1])
        self.assertTrue(os.path.exists(output_img_folder))
        self.assertTrue(os.path.isdir(output_img_folder))
        self.assertTrue(len(os.listdir(output_img_folder))>0)

if __name__ == "__main__":
    unittest.main()