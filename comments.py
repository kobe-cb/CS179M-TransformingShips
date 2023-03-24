import requests
from datetime import datetime

response = requests.get('http://worldtimeapi.org/api/ip')

current_time = datetime.fromisoformat(response.json()['datetime'])
user = 'Dylan'
manifestName = 'ShipCase1.txt'
outboundManifest = 'ShipCase1OUTBOUND.txt'
numContainers = 12
userComment = 'The container has a mismatched weight.'
currentContainerName = 'Cat'
positionToMove = '(1, 3)'


# Case 1: Log In
# Case 2: Log Out
# Case 3: Manifest is opened
# Case 4: Outbound Manifest Created
# Case 5: User Comment
# Case 6: Container is moved to a position INSIDE the ship
# Case 7: Container is unloaded
# Case 8: Container is loaded.
def log_write(case):
    with open('example.txt', 'a') as f:
        timestamp = current_time.strftime('%B %dth %Y: %H:%M ')
        if case == 1:
            comment = user + ' signs in.'
        if case == 2:
            comment = user + ' signs out.'
        if case == 3:
            comment = 'Manifest ' + manifestName + ' is opened, there are ' + str(
                numContainers) + ' containers on the ship.'
        if case == 4:
            comment = 'Finished a Cycle. Manifest ' + outboundManifest + ' was written to desktop, and a reminder pop-up to operator to send file was displayed.'
        if case == 5:
            comment = userComment
        if case == 6:
            comment = '"' + currentContainerName + '" moved to position ' + positionToMove + ' on the ship.'
        if case == 7:
            comment = '"' + currentContainerName + '" is offloaded.'
        if case == 8:
            comment = '"' + currentContainerName + '" is onloaded.'
        f.write(f'{timestamp} {comment}\n')


log_write(8)
