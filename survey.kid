<?xml version="1.0" encoding="iso-8859-1"?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
      xmlns:py="http://purl.org/kid/ns#">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1"/>
    <link rel="stylesheet" type="text/css" href="style.css"/>
    <title>${title}</title>
</head>
<body>


<h1>${title}</h1>

<div id="main">
    <form action="${SCRIPT_NAME}" method="post">

    <div py:if="not defined('result')" py:strip="">
        <fieldset>
            <legend>About you</legend>
            <b>Your name:</b> <input type="text" name="username" value="${username}" size="32" maxlength="40"/>
        </fieldset>

        <fieldset py:if="submitted">
            <legend>Errors</legend>
            <span class="warning">
                Only ${questions.numberAnswered()} of ${len(questions)} questions were answered so far.<br/>
                The remaining ${questions.numberUnanswered()} questions must be answered for final evaluation.
            </span>
        </fieldset>

        <fieldset py:for="i, q in enumerate(questions.getQuestions())">
            <legend>${i+1}. ${q.caption}</legend>
            <p py:if="submitted and not q.answered" class="warning">This question has not been answered yet.</p>
            <div py:for="a in q.getAnswers()" py:strip="">
            <input type="radio" id="q_${q.hash}__a_${a.hash}" name="q_${q.hash}" value="a_${a.hash}" checked="${a.selected and 'checked' or None}"/><label for="q_${q.hash}__a_${a.hash}">${a.caption}</label><br/>
            </div>
        </fieldset>

        <fieldset style="text-align: center;">
            <legend>Summary</legend>
            <input type="submit" value="Evaluate"/>
        </fieldset>
    </div>

    <div py:if="defined('result')" py:strip="">
        <fieldset style="text-align: center;">
            <legend>Summary</legend>
            <p style="font-weight: bold;">Your score, ${result.username or 'stranger'}:</p>
            <p class="result">${result.score}%</p>
            <p>${result.rating}</p>
            <p style="font-weight: bold;">[ <a href="${SCRIPT_NAME}">Start again</a> ]</p>
        </fieldset>
    </div>

    </form>
</div>

<p><small>Copyright &copy; 2005, 2006 Jochen Kupperschmidt</small></p>


</body>
</html>