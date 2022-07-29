const weekSelector = document.querySelector('#tip-week-selector')

weekSelector.addEventListener('input', function () {
    const week = weekSelector.value;
    location.href = '/tips' + week;
});


//get all individual tips
//add event listener click
//which will toggle a class 
//that turns the background color light grey

const individualTips = document.querySelectorAll('.individual-team-tip');

for (const tip of individualTips) {
    if (tip.dataset.completed == 'False') {
        tip.addEventListener('click', function () {
            tip.classList.toggle('tipped');
            const matchId = tip.dataset.match;
            const teams = document.querySelectorAll('[data-match=\"' + matchId + '\"]');
            const otherTeam = getOtherTeam(tip, teams);
            otherTeam.classList.remove('tipped');
        });
    }
}

function getOtherTeam(team1, teams) {
    for (const team of teams) {
        if (team != team1) {
            return team;
        }
    }
    return
}

const saveTipsButton = document.querySelector('#saveTips');

if (saveTipsButton != null) {
    saveTipsButton.addEventListener('click', function () {
        const tipsToEnter = document.querySelectorAll('.tipped');
        if (tipsToEnter.length == 0) {
            return
        }
        const form = document.createElement('form');
        form.method = 'post';
        form.action = '/enter_tips'
        let i = 0;
        for(let tip of tipsToEnter) {
            const match_id = tip.dataset.match;
            const team_tipped_id = tip.dataset.team;
            const input = document.createElement('input');
            input.name = String(i);
            input.value = match_id + ',' + team_tipped_id;
            form.appendChild(input);
            i++;
        }

        const formLength = form.children.length;
        const lengthInput = document.createElement('input');
        lengthInput.name = 'length';
        lengthInput.value = formLength;
        form.appendChild(lengthInput);;
        document.body.appendChild(form)
        form.submit();
    });
}

/*
on click of save tips button
collect all the divs that have the class 'tipped'
create a form
*/