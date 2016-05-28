Instructions:

- Please use requirements file with a Python 3.51 virtualenv for best results:
1. Create and activate your virtualenv in text_counter directory.
       Ubuntu 14.04.4 LTS:
           python3 -m venv env3
           source env3/bin/activate
2. Run the following to install dependencies:  "pip install -r ./docs/requirements.txt"
       Ubuntu 14.04.4 LTS:
           sudo apt-get install libncurses5-dev
3. Run the tests:
       py.test tests/test_word_count.py
4. Launch The IPython Notebook: "jupyter notebook demo_word_count.ipynb"
5. Try it out.

Thanks,

Chris Andrews
cwandrews.oh+cohpy@gmail.com
