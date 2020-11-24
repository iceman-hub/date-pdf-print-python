image_key = "5fb3ce22e84b1a686b555511"
# тот документ который не подходит 5fb3ce22e84b1a686b5554fc 
# матрица было создана для этого 5fb3ce22e84b1a686b55550c
href="http://api.sherlocktest.kt-team.de/api/pages/" + image_key
image_href = href + "/image/actual"
ocr_href = href + "/ocr"

image_name = "test.png"
basis = {
    'A': {'x': -26, 'y': 17},
    'B': {'x': 34, 'y': 17},
    'C': {'x': 13, 'y': 30}
}
