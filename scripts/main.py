import logging
import threading
import time
from readuino import *
import subprocess
from upload_photo import *
import os
import queue
from datetime import date

q = queue.Queue()

def manage_irrigation():
    port = os.getenv("PORT_I")
    outfile1 = os.getenv("OUT_M1")
    outfile2 = os.getenv("OUT_M2")
    t1 = 0
    t2 = 0
    tel = {}

    fo = open(outfile1, 'r')
    tel["t1"] = float(fo.read())
    
    fo.close()
    fo = open(outfile2, 'r')
    tel["t2"] = float(fo.read())
    fo.close()
    
    jlist = get_telemetry_irrigation(tel, port)
    #get_threshold_irrigation(jlist1, outfile1)
    #get_threshold_irrigation(jlist2, outfile2)
    q.put(jlist)
    
def manage_light_telemetry():
    port = os.getenv("PORT2")
    outfile1 = os.getenv("OUT_ML1")
    outfile2 = os.getenv("OUT_ML2")
    t1 = 0
    t2 = 0
    tel = {}

    fo = open(outfile1, 'r')
    tel["t1"] = float(fo.read())
    
    fo.close()
    fo = open(outfile2, 'r')
    tel["t2"] = float(fo.read())
    fo.close()
    
    jlist = get_telemetry(tel, port)

    #get_threshold_irrigation(jlist1, outfile1)
    #get_threshold_irrigation(jlist2, outfile2)

    q.put(jlist)

def manage_telemetry():
    port = os.getenv("PORT1")
    outfile1 = os.getenv("OUT_ML3")
    outfile2 = os.getenv("OUT_ML4")
    t1 = 0
    t2 = 0
    tel = {}

    fo = open(outfile1, 'r')
    tel["t1"] = float(fo.read())
    
    fo.close()
    fo = open(outfile2, 'r')
    tel["t2"] = float(fo.read())
    fo.close()
    
    jlist = get_telemetry(tel, port)

    #get_threshold_irrigation(jlist1, outfile1)
    #get_threshold_irrigation(jlist2, outfile2)
    q.put(jlist)

def manage_media():

    subprocess.call(['sh', './init_camera.sh'])
    bkt = os.getenv("BUCKET")
    idx1 = str(uuid.uuid4()) + '.jpg'
    upload_file('output/images/capture_1.jpg', bkt, idx1)
    idx2 = str(uuid.uuid4()) + '.jpg'
    upload_file('output/images/capture_2.jpg', bkt, idx2)
    idx3 = str(uuid.uuid4()) + '..mp4'
    os.system('sudo ffmpeg -framerate 24 -i output/videos/capture_vid4.h264 -c copy output/videos/capture_vid4.mp4')
    upload_file('output/videos/capture_vid4.mp4', bkt, idx3)
    os.system('rm -rf output/videos/capture_vid4.mp4')
    new_images = []
    greenhouse_id = int(os.getenv("GREENHOUSE"))
    level1 = int(os.getenv("LEVEL1"))
    level2 = int(os.getenv("LEVEL2"))
    user_id = os.getenv("USERID")
    plant1 = int(os.getenv("PLANT1"))
    plant2 = int(os.getenv("PLANT2"))
    media_url = os.getenv("MEDIA_URL")

    new_images.append({
        "greenhouse": greenhouse_id,
        "name": plants_list[plant1],
        "level": level1,
        "userid": user_id,
        "diagnosis": "healthy",
        "type": media_type[1],
        "url": media_url+idx1,
        "datetime": datetime.now()
        
    })
    new_images.append({
        "greenhouse": greenhouse_id,
        "name": plants_list[plant2],
        "level": level2,
        "userid": user_id,
        "diagnosis": "healthy",
        "type": media_type[1],
        "url": media_url+idx2,
        "datetime": datetime.now()

    })
    '''new_images.append({
        "greenhouse": greenhouse_id,
        "name": plants_list[0],
        "level": 0,
        "userid": user_id,
        "diagnosis": "healthy",
        "type": media_type[2],
        "url": media_url+idx3,
        "datetime": datetime.now()

    })'''
    insert_telemetry(new_images, im_records)

def process_telemetry():
    jlist = []
    greenhouse = int(os.getenv("GREENHOUSE"))
    userid = os.getenv("USERID")
    plant1 = int(os.getenv("PLANT1"))
    plant2 = int(os.getenv("PLANT2"))
    level1 = int(os.getenv("LEVEL1"))
    level2 = int(os.getenv("LEVEL2"))
    l2 = q.get()
    l1 = q.get()
    l_tel = q.get()
    moist1 = []
    moist2 = []
    for i in [0,1]:
        moist1.append([plant1, mean([l_tel[i]["moisture_1_1"], l_tel[i]["moisture_1_2"]])])
        jlist.append({"moisture": mean([l_tel[i]["moisture_1_1"], l_tel[i]["moisture_1_2"]]),
                      "temperature": l1[i]["temperature"],
                      "humidity": l1[i]["humidity"],
                      "altitude": l1[i]["altitude"],
                      "pressure": l1[i]["pressure"],
                      "light": l1[i]["light"],
                      "lpg": l1[i]["lpg"],
                      "co": l1[i]["co"],
                      "smoke": l1[i]["smoke"],
                      "greenhouse": greenhouse,
                      "userid": userid,
                      "plant": plants_list[plant1],
                      "level": level1
                      })
        moist2.append([plant2, mean([l_tel[i]["moisture_2_1"], l_tel[i]["moisture_2_2"]])])
        jlist.append({"moisture": mean([l_tel[i]["moisture_2_1"], l_tel[i]["moisture_2_2"]]),
                      "temperature": l2[i]["temperature"],
                      "humidity": l2[i]["humidity"],
                      "altitude": l2[i]["altitude"],
                      "pressure": l2[i]["pressure"],
                      "light": l1[i]["light"],
                      "lpg": l2[i]["lpg"],
                      "co": l2[i]["co"],
                      "smoke": l2[i]["smoke"],
                      "greenhouse": greenhouse,
                      "userid": userid,
                      "plant": plants_list[plant2],
                      "level": level2
                      })
    print(jlist)
    insert_telemetry(jlist, records)
    outfile1 = os.getenv("OUT_ML1")
    outfile2 = os.getenv("OUT_ML2")
    get_threshold_irrigation(moist1, outfile1)
    get_threshold_irrigation(moist2, outfile2)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    threads = list()
    x1 = threading.Thread(target=manage_irrigation)
    threads.append(x1)
    x2 = threading.Thread(target=manage_light_telemetry)
    threads.append(x2)
    x3 = threading.Thread(target=manage_telemetry)
    threads.append(x3)
    #x4 = threading.Thread(target=manage_media)
    #threads.append(x4)
    x1.start()
    x2.start()
    x3.start()
    #x4.start()

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)
    
    # Add telemetry to database
    process_telemetry()
