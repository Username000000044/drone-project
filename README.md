## Chat GPT Input:

```
I have a course that has colored tape on the ground and hoola-hoops dangling from the celing using string that aligns with the course on the ground. The hoops and the tape are color coded so around a 1/6 of the course is one color and the others is another color tape. Im attempting to navigate this course using a tello drone + python + opencv. I've attempted this twice before, once using just threads and another time using queues and  multi-processing to process the frames for a supposidly performance increase. Despite these claims, the video feed of the drones in open cv is always laggy and multiple seconds behind.  Is there any other ways to autonomously navigate the course using the tello drone so there is minimal delay and maximum efficency for not so powerful machines. Im open to ditching open cv completely and using av or some alterantive. The drone just needs to fly up, locate the hoola-hoops, find their center, and navigate through them. Some issues ive also experienced were that the drone couldnt see the entire hoola-hoop so I had to calculate a circle using the arc that is seen in the frames. Another issue is that some hoops are farther away than others and may be difficult to spot sometimes espiacally for one part of the course where teh next hoop is several feet away and would require the drone to rotate so it can navigate through it. Im using some school dell laptop. The lighting conditions are quite dim, which is another issue, but if need be, I can adjust the lights. There are around 6 colors around the course, red, orange, yellow, green, blue, and purple. The drone needs to complete the course by itself without assistance. All I need the ddrone to do is complete the course, however the course isnt a straight line and requires turning and etc. Im running windows so another software alternatives will work and I can adjust code to anything however I need to stick to python. Just as a reminder, im using djitellopy.
```

## Clone Repository:

```
git clone https://github.com/Username000000044/drone-project.git
cd drone-project

pip install -r requirements.txt
```

## Publish to Github:

```
git status
git add .
git commit -m "Describe your changes here"
git push origin main
```

## Adding Package:

```
pip install package
pip freeze > requirements.txt
```
