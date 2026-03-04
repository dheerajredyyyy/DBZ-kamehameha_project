"""Webcam-based Kamehameha effect using MediaPipe hands and OpenCV rendering."""

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import cv2
import mediapipe as mp
import numpy as np
import math
import random
import time
import pygame

# Audio and image assets loaded once at startup
pygame.mixer.init()

charge_sound = pygame.mixer.Sound("media/Basechargeloop1.wav")
escalate_sound = pygame.mixer.Sound("media/Escalation2.wav")
release_sound = pygame.mixer.Sound("media/Release3.wav")

logo_img = cv2.imread("media/logo.png", cv2.IMREAD_UNCHANGED)
background_img = cv2.imread("media/background.jpg")

# Simple state machine for the effect
IDLE="IDLE"
CHARGING="CHARGING"
FIRING="FIRING"
END="END"

# Global particle containers reused across frames
particles=[]
sparks=[]
streaks=[]
rings=[]

# Mouse state for end-screen interactions
mouse_clicked=False
mouse_x=0
mouse_y=0
escalate_played=False

charge_channel=None
escalate_channel=None
release_channel=None


def mouse_callback(event,x,y,flags,param):
    global mouse_clicked,mouse_x,mouse_y
    mouse_x=x
    mouse_y=y
    if event==cv2.EVENT_LBUTTONDOWN:
        mouse_clicked=True


def draw_logo(frame):

    if logo_img is None:
        return frame

    h,w=frame.shape[:2]

    logo=logo_img.copy()

    logo_width=int(w*0.3)
    scale=logo_width/logo.shape[1]

    logo=cv2.resize(logo,(0,0),fx=scale,fy=scale)

    lh,lw=logo.shape[:2]

    x=(w-lw)//2
    y=h-lh-40

    if logo.shape[2]==4:

        alpha=logo[:,:,3]/255.0

        for c in range(3):
            frame[y:y+lh,x:x+lw,c]=(
                alpha*logo[:,:,c]+
                (1-alpha)*frame[y:y+lh,x:x+lw,c]
            )
    else:
        frame[y:y+lh,x:x+lw]=logo

    return frame


def stop_all_sounds():

    global charge_channel,escalate_channel,release_channel,escalate_played

    if charge_channel:
        charge_channel.fadeout(200)

    if escalate_channel:
        escalate_channel.fadeout(200)

    if release_channel:
        release_channel.fadeout(200)

    escalate_played=False


def bloom(frame,mask,strength):

    small=cv2.resize(mask,None,fx=0.3,fy=0.3)
    small=cv2.GaussianBlur(small,(0,0),sigmaX=12)

    bloom=cv2.resize(small,(frame.shape[1],frame.shape[0]))

    return cv2.addWeighted(frame,1,bloom,strength,0)


def heat_distortion(frame,center,radius):

    h,w=frame.shape[:2]
    cx,cy=center

    y,x=np.indices((h,w))

    dx=x-cx
    dy=y-cy

    dist=np.sqrt(dx**2+dy**2)
    mask=dist<radius

    power=(radius-dist)/radius
    power[~mask]=0

    offset=power*5*np.sin(dist*0.08)

    map_x=(x+offset).astype(np.float32)
    map_y=(y+offset).astype(np.float32)

    return cv2.remap(frame,map_x,map_y,cv2.INTER_LINEAR)


def update_particles(frame,center):

    cx,cy=center

    if len(particles)<900:

        for _ in range(20):

            angle=random.uniform(0,2*math.pi)
            dist=random.uniform(160,380)

            particles.append([angle,dist])

    for p in particles:

        angle,dist=p

        angle+=0.05
        dist-=2.2

        if dist<30:

            angle=random.uniform(0,2*math.pi)
            dist=random.uniform(220,420)

        p[0]=angle
        p[1]=dist

        x=int(cx+math.cos(angle)*dist)
        y=int(cy+math.sin(angle)*dist)

        size=random.randint(2,4)

        cv2.circle(frame,(x,y),size,(255,255,210),-1)


def update_streaks(frame,center):

    cx,cy=center

    if len(streaks)<40:

        angle=random.uniform(0,2*math.pi)
        dist=random.uniform(200,420)

        streaks.append([angle,dist])

    for s in streaks:

        angle,dist=s

        angle+=0.1
        dist-=3

        if dist<50:

            s[0]=random.uniform(0,2*math.pi)
            s[1]=random.uniform(240,420)
            continue

        s[0]=angle
        s[1]=dist

        x1=int(cx+math.cos(angle)*dist)
        y1=int(cy+math.sin(angle)*dist)

        x2=int(cx+math.cos(angle)*(dist+30))
        y2=int(cy+math.sin(angle)*(dist+30))

        cv2.line(frame,(x1,y1),(x2,y2),(255,220,150),2)


def update_sparks(frame,center):

    cx,cy=center

    if len(sparks)<120:

        for _ in range(5):

            angle=random.uniform(0,2*math.pi)
            speed=random.uniform(4,8)

            sparks.append([cx,cy,angle,speed])

    new=[]

    for s in sparks:

        x,y,a,sp=s

        x+=math.cos(a)*sp
        y+=math.sin(a)*sp

        sp*=0.94

        if sp>1:

            new.append([x,y,a,sp])

            cv2.circle(frame,(int(x),int(y)),2,(255,240,200),-1)

    sparks[:] = new


def draw_aura_rings(frame,center,radius):

    if len(rings)<3:

        for i in range(3):
            rings.append(random.uniform(0,360))

    for i in range(len(rings)):

        rings[i]+=2+i

        axes=(radius+60+i*25,int((radius+60+i*25)*0.35))

        cv2.ellipse(
            frame,
            center,
            axes,
            rings[i],
            0,
            360,
            (255,220,160),
            2,
            cv2.LINE_AA
        )


def draw_arcs(frame,center,radius):

    cx,cy=center

    for _ in range(random.randint(4,7)):

        a=random.uniform(0,2*math.pi)

        r1=random.uniform(radius*0.6,radius)
        r2=r1+random.uniform(20,60)

        x1=int(cx+math.cos(a)*r1)
        y1=int(cy+math.sin(a)*r1)

        x2=int(cx+math.cos(a)*r2)
        y2=int(cy+math.sin(a)*r2)

        cv2.line(frame,(x1,y1),(x2,y2),(255,230,160),2)


def shake(frame):

    h,w=frame.shape[:2]

    dx=random.randint(-6,6)
    dy=random.randint(-6,6)

    M=np.float32([[1,0,dx],[0,1,dy]])

    return cv2.warpAffine(frame,M,(w,h))


def draw_ball(frame,center,hand_dist):

    cx,cy=center

    radius=int(hand_dist*0.8)
    radius=max(120,radius)
    radius=min(radius,420)

    glow=np.zeros_like(frame)

    cv2.circle(frame,(cx,cy),radius,(255,200,80),-1)
    cv2.circle(frame,(cx,cy),int(radius*0.6),(255,255,230),-1)

    cv2.circle(glow,(cx,cy),radius+90,(255,255,255),-1)

    draw_arcs(frame,(cx,cy),radius)
    draw_aura_rings(frame,(cx,cy),radius)

    update_particles(frame,(cx,cy))
    update_streaks(frame,(cx,cy))

    if radius>350:
        update_sparks(frame,(cx,cy))

    frame=bloom(frame,glow,0.9)

    blue=np.zeros_like(frame)
    cv2.circle(blue,(cx,cy),radius+320,(255,130,40),-1)

    frame=cv2.addWeighted(frame,1,blue,0.18,0)

    frame=heat_distortion(frame,(cx,cy),radius+150)

    return frame,radius


def explosion(frame,origin,elapsed):

    h,w=frame.shape[:2]
    cx,cy=origin

    if elapsed<0.6:

        progress=elapsed/0.6
        radius=int(progress*math.hypot(w,h))

        shock=np.zeros_like(frame)
        cv2.circle(shock,(cx,cy),radius,(255,255,255),-1)

        return cv2.addWeighted(frame,1,shock,1.2,0)

    # After the shockwave, fill with a bright frame for the final flash
    return np.full_like(frame,(255,240,180))


def draw_end_screen(frame,mouse_clicked,mouse_pos):

    h,w,_=frame.shape
    mx,my=mouse_pos

    # Scale and crop the background art so it always fills the frame
    if background_img is not None:
        bh,bw=background_img.shape[:2]

        scale=max(w/bw,h/bh)
        new_w=int(bw*scale)
        new_h=int(bh*scale)

        bg_resized=cv2.resize(background_img,(new_w,new_h))

        x_start=(new_w-w)//2
        y_start=(new_h-h)//2
        bg_cropped=bg_resized[y_start:y_start+h,x_start:x_start+w]

        frame[:]=bg_cropped
    else:
        frame[:]=(255,240,180)

    title_font=cv2.FONT_HERSHEY_SIMPLEX
    ui_font=cv2.FONT_HERSHEY_SIMPLEX

    title="POWER UNLEASHED"
    title_scale=2.1
    tsize=cv2.getTextSize(title,title_font,title_scale,5)[0]

    tx=(w-tsize[0])//2
    ty=int(h*0.47)

    shadow_color=(0,0,0)
    for dx,dy in [(-3,0),(3,0),(0,-3),(0,3),(3,3)]:
        cv2.putText(
            frame,
            title,
            (tx+dx,ty+dy),
            title_font,
            title_scale,
            shadow_color,
            6,
            cv2.LINE_AA
        )

    cv2.putText(
        frame,
        title,
        (tx,ty),
        title_font,
        title_scale,
        (255,255,255),
        6,
        cv2.LINE_AA
    )

    btn_text="TRY AGAIN"
    btn_scale=1.1
    bsize=cv2.getTextSize(btn_text,ui_font,btn_scale,2)[0]

    bx=(w-bsize[0])//2
    by=int(h*0.58)

    pad_x=60
    pad_y=28

    btn_x1=bx-pad_x
    btn_y1=by-pad_y
    btn_x2=bx+bsize[0]+pad_x
    btn_y2=by+pad_y

    is_hover=btn_x1<=mx<=btn_x2 and btn_y1<=my<=btn_y2
    is_pressed=mouse_clicked and is_hover

    base_color=(26,26,26)        # #1A1A1A (dark button)
    hover_color=(0,106,255)      # #FF6A00 (orange, BGR)
    press_color=(0,90,210)       # slightly darker orange

    btn_color=base_color
    if is_pressed:
        btn_color=press_color
    elif is_hover:
        btn_color=hover_color

    cv2.rectangle(
        frame,
        (btn_x1,btn_y1),
        (btn_x2,btn_y2),
        btn_color,
        -1
    )

    # Button border for definition
    cv2.rectangle(
        frame,
        (btn_x1,btn_y1),
        (btn_x2,btn_y2),
        (60,60,60),
        2
    )

    cv2.putText(
        frame,
        btn_text,
        (bx,by+6),
        ui_font,
        btn_scale,
        (255,255,255),
        2,
        cv2.LINE_AA
    )

    # Developer mark (bottom-center, subtle)
    watermark="@Developed by Dheeraj Reddy"
    wm_scale=0.7
    wsize=cv2.getTextSize(watermark,ui_font,wm_scale,1)[0]

    wx=(w-wsize[0])//2
    wy=h-80

    cv2.putText(
        frame,
        watermark,
        (wx,wy),
        ui_font,
        wm_scale,
        (191,191,191),
        1,
        cv2.LINE_AA
    )

    # Only the TRY AGAIN button triggers a reset
    clicked_try_again=is_pressed

    return frame,clicked_try_again


def main():

    global mouse_clicked,escalate_played
    global charge_channel,escalate_channel,release_channel

    # Open default webcam
    cap=cv2.VideoCapture(0)

    mp_hands=mp.solutions.hands

    # Lightweight hand tracker, up to two hands
    hands=mp_hands.Hands(
        max_num_hands=2,
        model_complexity=0,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6
    )

    # High-level state for the effect
    state=IDLE
    fire_start=None
    origin=None

    cv2.namedWindow("Kamehameha")
    cv2.setMouseCallback("Kamehameha",mouse_callback)

    # Main capture and render loop
    while True:

        ret,frame=cap.read()
        if not ret:
            break

        frame=cv2.flip(frame,1)

        h,w,_=frame.shape
        now=time.time()

        rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        res=hands.process(rgb)

        palms=[]

        if res.multi_hand_landmarks:

            for lm in res.multi_hand_landmarks:

                wrist=lm.landmark[0]

                x=int(wrist.x*w)
                y=int(wrist.y*h)

                palms.append((x,y))

        if state in [IDLE,CHARGING]:
            frame=draw_logo(frame)

        if state in [IDLE,CHARGING]:

            if len(palms)==2:

                center=((palms[0][0]+palms[1][0])//2,
                        (palms[0][1]+palms[1][1])//2)

                hand_dist=math.dist(palms[0],palms[1])

                if state==IDLE and hand_dist<300:

                    state=CHARGING
                    charge_channel=charge_sound.play(-1)

                if state==CHARGING:

                    frame,radius=draw_ball(frame,center,hand_dist)

                    charge_sound.set_volume(min(radius/400,1))

                    if radius>260 and not escalate_played:

                        escalate_channel=escalate_sound.play()
                        escalate_played=True

                    if radius>320:
                        frame=shake(frame)

                    if radius>380:

                        stop_all_sounds()

                        release_channel=release_sound.play()

                        state=FIRING
                        fire_start=now
                        origin=center

            else:

                stop_all_sounds()
                particles.clear()
                state=IDLE

        elif state==FIRING:

            elapsed=now-fire_start

            frame=explosion(frame,origin,elapsed)

            if elapsed>1.2:
                state=END

        elif state==END:

            frame,clicked_try_again=draw_end_screen(
                frame,
                mouse_clicked,
                (mouse_x,mouse_y)
            )

            # End screen consumes pointer events so they
            # do not affect the game underneath.
            if mouse_clicked:
                mouse_clicked=False

            if clicked_try_again:

                particles.clear()
                sparks.clear()
                streaks.clear()
                rings.clear()
                stop_all_sounds()
                escalate_played=False

                state=IDLE

        cv2.imshow("Kamehameha",frame)

        if cv2.waitKey(1)&0xFF==ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__=="__main__":
    main()