# latex2gift
LaTeX to GIFT format Conversor

Tool developed in Python, quizzes written in LaTeX and transformed into GIFT language in order to make them as usable and standard as possible.

An e-learning tool developed in Python, that helps groups of students learn the statistical package R in an autonomous manner. Self-assessment is an important part of R-QUEST; it is based on a set of lessons and quizzes written in LaTeX and transformed into GIFT language in order to make them as usable and standard as possible. Then the set of quizzes in GIFT format is imported to the Moodle Educational Platform, where they are made available to the students.

### LaTeX Special document formatted

For this tool works needs put some "special" sections into your document, like this:

```
\begin{introtest}
   \titletest(<title>)
   \adaptativetest(<YES|NO>)
   \timetest(<time>)
\end{introtest}
  
\newquestion

\newquestion
```
