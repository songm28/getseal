import getseal
import os, argparse, sys, re
import pandas as pd


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "-folder",
        dest="folder",
        default=None,
        help="source pdf file folder",
    )
    args = parser.parse_args()
    pdf_file_folder = args.folder
    target_seal_folder = os.path.join("imgs")
    result_file="seal_result.csv"

    df = pd.DataFrame()
    if pdf_file_folder is None or not os.path.exists(pdf_file_folder):
        # df.to_csv(result_file, index=False, header=True)
        print("Source file folder {} is invalid!".format(pdf_file_folder))
        sys.exit(1)

    for f in os.listdir(pdf_file_folder):
        f_path = os.path.join(pdf_file_folder, f)
        getseal.main(input_pdf=f_path, output_img_folder=target_seal_folder, pages=[0])
    
    # if not os.path.exists(target_seal_folder):
    #     # df.to_csv(result_file, index=False, header=True)
    #     print("Source file folder {} is invalid!".format(pdf_file_folder))
    #     sys.exit(2)

    source_filename_list = [x.lower() for x in os.listdir(pdf_file_folder)]
    seal_filename_list = list()
    if os.path.exists(target_seal_folder) and os.path.isdir(target_seal_folder): 
        pattern="seal__([^\.]+)_\d+\.png"
        # seal_filename_list = [x.lower()[6:-4] for x in os.listdir(target_seal_folder) if x.startswith("seal__") and x.endswith(".png")]
        seal_filename_list = [re.match(pattern, x).groups()[0] for x in os.listdir(target_seal_folder) if re.match(pattern, x) is not None]
        seal_filename_list = list(set(seal_filename_list))
    df["PDF"] = source_filename_list
    df["seal?"] = df["PDF"].apply(lambda x: "Yes" if x[:-4] in seal_filename_list else "No")
    df.to_csv(result_file, index=False, header=True)

    

    