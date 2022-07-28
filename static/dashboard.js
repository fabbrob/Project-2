leaderboardDiv = document.querySelector('#leaderboard')
enterTipsDiv = document.querySelector('#enterTips')
buttonLocation = enterTipsDiv.dataset.week
leaderboardDiv.addEventListener('click', function () {
    location.href = '/leaderboard'
})

enterTipsDiv.addEventListener('click', function () {
    location.href = '/tips/' + buttonLocation
})