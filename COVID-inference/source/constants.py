MODE = "mode"
TRAIN = "train"
PREDICT = "predict"
MODEL_NAME = "covid_model"
VERBOSE = "verbose"
MEAN_AGE = "mean_age"
TRAIN_PATH = "train_path"
TEST_PATH = "test_path"
simptom_dict = {"febra": 0,
  "durere abdominala": 1,
  "dureri epigastrice": 1,
  "durere retrosternala": 2,
  "dureri precordiala": 2,
  "mialgii": 3,
  "dureri musculare": 3,
  "durere in gat": 4,
  "durere toracica": 5,
  "greata":6,
  "frisoane":7,
  "inapetenta":8,
  "astenia":9,
  "erizipel":10,
  "parestezii":11,
  "disfagie":12,
  "palpitatii":13,
  "transpiratii":14,
  "vertij":15,
  "ameteli":15,
  "tuse": 16,
  "subfebrilitati": 0,
  "subfebril": 0,
  "febril": 0,
  "astenie": 17,
  "dispnee": 18,
  "cefalee": 18,
  "durere de cap": 18,
  "varsaturi": 19,
  "dificultati de respiratie": 18,
  "diaree": 20,
  "scaun": 20,
  "frison": 21,
  "temperatura <>": 22,
  "temp <>": 22,
  "hematemeza": 23,
  "icter": 24,
  "inapententa": 25,
  "lipsa de gust": 25}