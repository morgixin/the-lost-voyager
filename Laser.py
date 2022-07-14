class Laser:
    def __init__(self, x, y, img):
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.topleft = [x, y]

    def update(self, window):
        window.blit(self.img, (self.rect.x, self.rect.y))
    
    def move(self, speed):
        self.rect.y += speed
    
    def collision(self, obj):
        return self.collide(self, obj)

    def offscreen(self):
        return not(self.rect.y <= 500 and self.rect.y >= 0)

    def collide(obj1, obj2):    
        return obj1.rect.colliderect(obj2)