import pygame , sys , pytmx
pygame.init()

#Variables init

clock=pygame.time.Clock()
WINDOWWIDTH = 600
WINDOWHEIGHT = 400
running=True
playerSprite=pygame.image.load("player\\playertmpst.png")
playerSprite=pygame.transform.scale2x(playerSprite)
SKY=(134 , 219 , 251)
playerPos=[100,50]
movingRight=False
movingLeft=False
isJumping=False
moveSpeed=3
global jumpCount
jumpCount=9
pygame.mixer.init()
pygame.mixer.music.load("Songs\\main.wav")
pygame.mixer.music.play(-1)
#Variables init End

#Screen init
screen = pygame.display.set_mode((WINDOWWIDTH , WINDOWHEIGHT))

pygame.display.set_caption("platformer")
#Screen init End

#Tilemap loader
gameMap=pytmx.load_pygame("TilesetnMap\\GameMap.tmx")
#Tilemap loader End

#MainLoop

while running:

    isFalling=True
    isCollidingLeft=False
    isCollidingRight=False
    isJumping=False
    playerRect=playerSprite.get_rect()
    playerRect.x=playerPos[0]
    playerRect.y=playerPos[1]
    screen.fill(SKY)  # Change background color to sky blue color
    clock.tick(60)
    # TileMap Renderer start
    for layer in gameMap.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = gameMap.get_tile_image_by_gid(gid)
                if tile != None:
                    screen.blit(tile, (x * gameMap.tilewidth, y * gameMap.tileheight))

        if isinstance(layer,pytmx.TiledObjectGroup):

            for obj in layer:
                if(obj.name=="Platforms"):
                    if pygame.Rect(obj.x,obj.y,obj.width,obj.height).colliderect(playerRect):
                        isFalling=False
                if(obj.name=="Left walls"):
                    if pygame.Rect(obj.x, obj.y, obj.width, obj.height).colliderect(playerRect):
                        isCollidingLeft=True

                if (obj.name == "Right walls"):
                    if pygame.Rect(obj.x, obj.y, obj.width, obj.height).colliderect(playerRect):
                        isCollidingRight = True

    # TileMap Renderer End
    for event in pygame.event.get():#Getting the events
        if event.type == pygame.QUIT:#Checking if user has clicked X button on the window or not
            pygame.quit()
            sys.exit()
            running = False

    if event.type==pygame.KEYDOWN:#Check if any key is pressed do

        if event.key==pygame.K_RIGHT:
            movingRight=True
        if event.key==pygame.K_LEFT:
            movingLeft=True
        if event.key==pygame.K_UP:
            isJumping=True

    if event.type==pygame.KEYUP:#Check if any key is released

        if event.key==pygame.K_RIGHT:
            movingRight=False
        if event.key==pygame.K_LEFT:
            movingLeft=False

    if movingRight and not isCollidingRight: #If the player is moving Right and not colliding on the right side
        movingRight=True
    if movingLeft and not isCollidingLeft:#If the player is moving Left and not colliding on the left side
        movingLeft=True

    if isCollidingRight:
        movingRight=False
    if isCollidingLeft:
        movingLeft=False

    if movingRight :
        playerPos[0] += moveSpeed#Move right

    if movingLeft :
        playerPos[0]-= moveSpeed#move left

    if(isFalling):#Gravity of player
        playerPos[1]+=3

    if isJumping and not isCollidingRight and not isCollidingLeft:
        if jumpCount>=-9:
            neg=1
            playerPos[1]-=jumpCount**2*0.1*neg
            jumpCount-=1
            if jumpCount<0:
                neg=-1
        else:
            isJumping=False
            jumpCount=9

    screen.blit(playerSprite,playerRect)#Load player sprite
    pygame.display.update()
    pygame.display.flip()#Makes the window visible
#MainLoop End

