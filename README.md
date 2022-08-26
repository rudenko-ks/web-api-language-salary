# Comparing the salaries of programmers

Get developer vacancies from HeadHunter and SuperJob and calculate the average salary for each program language:

![enter image description here](https://github.com/rudenko-ks/web-api-language-salary/blob/main/output_example.jpg)

### Install

Python3 should already be installed.
1. Clone the repository
```
git clone https://github.com/rudenko-ks/web-api-language-salary
```
2. Create a virtual environment
```
python -m venv .venv
source .venv/bin/activate
```
3. Use `pip` to install dependencies
```
pip install -r requirements.txt
```
4. Create an environment variable file `.env` in the project directory with the following content:
```
SUPERJOB_API_TOKEN=<ENTER YOUR SUPERJOB API TOKEN HERE>
```
5. Run the script
```
python main.py
```

### Project Goals

The code is written for educational purposes on online-course for web-developers  [dvmn.org](https://dvmn.org/)
