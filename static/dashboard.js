tipsDiv = document.querySelector('#tips')
leaderboardDiv = document.querySelector('#leaderboard')

tipsDiv.addEventListener('click', function () {
    location.href = '/tips'
})

leaderboardDiv.addEventListener('click', function () {
    location.href = '/leaderboard'
})