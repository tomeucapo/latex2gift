# latex2gift
LaTeX to GIFT format Conversor

Tool developed in Python, quizzes written in LaTeX and transformed into GIFT language in order to make them as usable and standard as possible.

An e-learning tool developed in Python, that helps groups of students learn the statistical package R in an autonomous manner. Self-assessment is an important part of R-QUEST; it is based on a set of lessons and quizzes written in LaTeX and transformed into GIFT language in order to make them as usable and standard as possible. Then the set of quizzes in GIFT format is imported to the Moodle Educational Platform, where they are made available to the students.

### LaTeX Special document formatted

For this tool works needs put some "special" sections into your document with pre-declared commands at the document header:
```
\newcommand{\answer}{\textbf{Resposta: }}
\newcommand{\titletest}[1]{\centerline{\Large\textbf{#1}}\medskip}
\newcommand{\timetest}[1]{\noindent\textbf{Temps:} #1 minuts}
\newcommand{\questionstest}{\noindent\textbf{Qüestions: }}
\newcommand{\adaptativetest}{\noindent\textbf{Mode adaptatiu: }}
\newcommand{\newquestion}[2]{\noindent\textbf{Qüestió: }\emph{#1} \textbf{Tipus: }\emph{#2}\medskip}
\newenvironment{introtest}{}{\newpage}
\newcommand{\transw}{\hspace*{1cm} Vertadera}
\newcommand{\namequestion}{}
```

And use, like this:

```
\begin{introtest}
   \titletest <title> 
   \adaptativetest <YES|NO>
   \timetest <time> 
\end{introtest}
  
\namequestion{qintr1-01}
\qintro1{la funció exp}\\ 
\answer{\verb?help("exp") log?}\\

```
