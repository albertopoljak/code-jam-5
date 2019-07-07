import pyglet


class TextBox:
    '''
    A convenience wrapper around a pyglet sprite and label.
    '''

    def __init__(self, text, text_box_image, color=(255, 255, 255, 255), label_x=0, label_y=0, font_name='',
                 font_size=None,
                 screen_width=640):
        self.text = text
        self.image = text_box_image
        self.color = color
        self.label_x = label_x
        self.width = screen_width
        # Draw at the top of the sprite, with offset
        self.label_y = self.image.height - label_y

        self.label = pyglet.text.Label(
            self.text,
            x=self.label_x,
            y=self.label_y,
            anchor_y='top',
            multiline=True,
            width=(self.width - self.label_x),
            color=color,
            font_name=font_name,
            font_size=font_size)
        self.sprite = pyglet.sprite.Sprite(self.image)

    def draw(self):
        self.sprite.draw()
        self.label.draw()
