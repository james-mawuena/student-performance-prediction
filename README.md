# Student Final CGPA Predictor

Predicting a student's final CGPA, and which degree class they are likely to graduate with, from their first-year results.

**Live demo:** https://student-cgpa-predictor.streamlit.app/

## What this project does

A student enters their first-year CGPA, their secondary school grade, and their program of study. The app returns two things:

- An estimate of their final CGPA (linear regression)
- The most likely degree class (First, Second Upper, Second Lower or Third) and the chance for each class (logistic regression)

The idea is an early warning: a school could use this to notice which students may need extra support after first year.

## Data

The data is the "Dataset on the academic performance of students in 12 programs from a private university" by Roseline Ogundokun and Cristian Ramos-Vera (Mendeley Data, 2020, DOI: 10.17632/dp8cywvp8y.1). It covers 3,046 graduates of Landmark University, Nigeria, across 17 programs, graduating between 2010 and 2014.

All grades in this dataset (first-year CGPA, final CGPA and secondary school grade) are on a 5.0 scale, not a 4.0 scale. The models and the app only make sense for grades on a 5.0 scale.

The data file is included in this repository, unchanged, so the notebook can run as it is. It is shared under the [Creative Commons Attribution 4.0 (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) licence. Full credit goes to the original authors, and the original source is on [Mendeley Data](https://data.mendeley.com/datasets/dp8cywvp8y/1).

## Method

**Inputs:** first-year CGPA, secondary school grade, and program of study (turned into one yes/no column per program).

**Degree classes:** First (CGPA 4.50 and above), Second Upper (3.50 to 4.49), Second Lower (2.40 to 3.49) and Third (1.50 to 2.39), using the commonly used 5.0-scale cut-offs. No student in the data was below 1.50.

**Left out on purpose:**
- Gender. The tool is meant to flag students who need help, so it should not judge anyone by gender. See the fairness check below.
- CGPA at the end of years 2, 3 and 4. These are part of the final CGPA, so using them would make the score look good without meaning anything.

**Testing:** 80% of students (2,436) were used to train the models. The other 20% (610) were hidden and used only for testing, so the scores show how the models do on students they have not seen.

## Results

| Model | Question | Score | Simple guess to beat |
| --- | --- | --- | --- |
| Linear regression | What will the final CGPA be? | Average error of 0.31 CGPA points | 0.59 (guessing the average for everyone) |
| Logistic regression | Which degree class? | 72% correct | 43% (guessing "Second Upper" for everyone) |

The linear regression score was checked again on 5 shuffled splits of the data and stayed stable (R2 between 0.68 and 0.71, average 0.69).

How many of the real students in each class the degree class model found:

| Class | Real students in the test group | Found by the model |
| --- | --- | --- |
| Third | 47 | 19% |
| Second Lower | 257 | 77% |
| Second Upper | 264 | 78% |
| First | 42 | 64% |

The model does well on the two large classes and finds about 1 in 5 Third Class students. Every wrong answer was one class away from the real one: no Third Class student was called Second Upper or First, and no First Class student was called Third or Second Lower.

## Fairness check

Gender was not used by the models, but the results were checked by gender on the 610 test students.

| Group | Students | Average CGPA error | Degree class right | Good degree: real | Good degree: model said |
| --- | --- | --- | --- | --- | --- |
| Female | 215 | 0.305 | 73.5% | 64% | 55% |
| Male | 395 | 0.319 | 71.4% | 43% | 50% |

"Good degree" means a CGPA of 3.5 or more (First or Second Upper).

The size of the errors is about the same for both groups. But the model leans slightly low for women (about 0.14 CGPA points too low on average) and slightly high for men (about 0.12 too high). In this data, women and men start first year at a similar level, but women finish higher on average, and a model that cannot see gender cannot account for that. The degree class answer is also right about equally often for both groups.

## Limitations

- The data comes from one private university and one group of graduation years (2010 to 2014), so the models may not work for other schools or later years.
- The models only use three inputs. They cannot see what happens to a student after first year, so they will miss students whose path changes a lot.
- When the models were tested on students from different graduation years than the ones they learned from, the score dropped (R2 about 0.58 instead of 0.69).
- The test group has only 215 women, so the fairness gaps are small and could change with different students.

## Run it yourself

```
pip install -r requirements.txt
streamlit run app.py
```

## Files

- `Dataset on the academic performance of students in 12 programs from a private university.xlsx`: the original data file, unchanged
- `student_performance_prediction.ipynb`: the full notebook, from loading the data to saving the models
- `app.py`: the Streamlit web app
- `model.pkl`: the trained linear regression model
- `degree_class_model.pkl`: the trained logistic regression model for the four degree classes
- `columns.pkl`: the list of input columns the models expect
- `requirements.txt`: the tools the app needs

## Author

James-Mawuena Abraham, Computer Engineering, Federal University of Technology, Akure. [LinkedIn](https://www.linkedin.com/in/jamesmawuena)
