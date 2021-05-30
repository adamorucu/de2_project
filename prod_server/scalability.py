from worker import add_nums, get_prediction

if __name__ == '__main__':
    prediction = get_prediction_scale.delay(2018, 90, 0, 0, 0, 20, 666, 1000)
    a = prediction.get()
