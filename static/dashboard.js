leaderboardDiv = document.querySelector('#leaderboard')
enterTipsDiv = document.querySelector('#enterTips')

leaderboardDiv.addEventListener('click', function () {
    location.href = '/leaderboard'
})

enterTipsDiv.addEventListener('click', function () {
    location.href = '/tips'
})