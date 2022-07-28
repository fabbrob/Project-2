leaderboardDiv = document.querySelector('#leaderboard')
enterTipsDiv = document.querySelector('#enterTips')
enterTipsButtonLocation = enterTipsDiv.dataset.week
viewResultsDiv = document.querySelector('#viewResults')
viewResultsButtonLocation = viewResultsDiv.dataset.week

leaderboardDiv.addEventListener('click', function () {
    location.href = '/leaderboard'
})

enterTipsDiv.addEventListener('click', function () {
    location.href = '/tips' + String(enterTipsButtonLocation)
})

if (viewResultsDiv != null) {
    viewResultsDiv.addEventListener('click', function () {
        location.href = '/tips' + String(viewResultsButtonLocation)
    })
}