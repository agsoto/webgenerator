import random
from Randomization.RandomHelper import RandomHelper
from Layout.WebLayout import WebLayout
from StyleManager.ColorManager import ColorManager

class WebLayoutChoices:
    class ShadowClasses:
        Shadow = "shadow"
        ShadowSm = "shadow-sm"
        ShadowLg = "shadow-lg"

    layouts = [1,2,3,4]
    boxed_wrapper_limits = { "x":[1, 10], "y":[1, 5]}
    sizes_limits = {
        "header":[16,40],
        "big-header":[50,100],
        "navbar":[3, 10],
        "sidebar":[22, 30], #Note: Depends on page aspect ratio
        "footer":[5, 30],
    }

    color_classes_style_choices = [ColorManager.ClassesStyle.Default, ColorManager.ClassesStyle.Inverse, ColorManager.ClassesStyle.NoLimits]
    bg_color_classes_p = [0.6,0.2,0.2]

    shadow_classes_choices = [ShadowClasses.Shadow, ShadowClasses.ShadowSm, ShadowClasses.ShadowLg]

wlc = WebLayoutChoices

class WebLayoutProbabilities:
    def __init__(self,with_sidebar_p, with_header_p, with_navbar_p, with_footer_p, 
    layouts_p,boxed_body_p,generate_alert_p, big_header_p, sidebar_first_p, navbar_first_p,bg_color_classes_p):
        self.with_sidebar_p = with_sidebar_p
        self.with_header_p = with_header_p
        self.with_navbar_p = with_navbar_p
        self.with_footer_p = with_footer_p
        self.layouts_p = layouts_p
        self.boxed_body_p = boxed_body_p
        self.big_header_p = big_header_p
        self.sidebar_first_p = sidebar_first_p
        self.navbar_first_p = navbar_first_p
        self.bg_color_classes_p = WebLayoutChoices.bg_color_classes_p
        if bg_color_classes_p is not None:
            self.bg_color_classes_p = bg_color_classes_p

    def weblayout_options_specific(self):
        specific = WebLayout(self.boxed_wrapper_specific(), 
            self.layout_specific(),
            self.sidebar_first_specific(), 
            self.navbar_first_specific(), 
            self.sizes_specific(self.with_sidebar_specific(), self.with_header_specific(), self.with_navbar_specific(), self.with_header_specific())
        )
        return specific

    def boxed_wrapper_specific(self):
        boxed = RandomHelper.flip_coin(self.boxed_body_p)
        if not boxed:
            return None
        symmetrical_x_y = RandomHelper.flip_coin() 
        if symmetrical_x_y:
            x = random.randint(wlc.boxed_wrapper_limits["x"][0],wlc.boxed_wrapper_limits["x"][1])
            y = x
        else:
            x = random.randint(wlc.boxed_wrapper_limits["x"][0],wlc.boxed_wrapper_limits["x"][1])
            if RandomHelper.flip_coin():
                y = random.randint(wlc.boxed_wrapper_limits["y"][0],wlc.boxed_wrapper_limits["y"][1])
            else:
                y = 0

        return {"x": x, "y": y} 
            

    def layout_specific(self):
        if self.layouts_p is None:
            return random.randint(min(wlc.layouts), max(wlc.layouts))
        else:
            assert len(self.layouts_p) == len(wlc.layouts), "Number of probability elements is different than number of layout elements"
            return random.choice(self.layouts_p, wlc.layouts)
    
    def with_sidebar_specific(self):
        return RandomHelper.flip_coin(self.with_sidebar_p)

    def with_header_specific(self):
        return RandomHelper.flip_coin(self.with_header_p)

    def with_navbar_specific(self):
        return RandomHelper.flip_coin(self.with_navbar_p)

    def with_footer_specific(self):
        return RandomHelper.flip_coin(self.with_footer_p)

    def sizes_specific(self, with_sidebar, with_header, with_navbar, with_footer):
        dictionary = {}
        if with_sidebar:
            dictionary["sidebar"] = random.randint(wlc.sizes_limits["sidebar"][0], wlc.sizes_limits["sidebar"][1])
        if with_header:
            head_key_selector = "header"
            if self.big_header_p is not None:
                big_header = RandomHelper.flip_coin(self.big_header_p)
                if big_header:
                    head_key_selector = "big_header"
            dictionary["header"] = random.randint(wlc.sizes_limits[head_key_selector][0], wlc.sizes_limits[head_key_selector][1])
        if with_navbar:
            dictionary["navbar"] = random.randint(wlc.sizes_limits["navbar"][0], wlc.sizes_limits["navbar"][1])
        if with_footer:
            dictionary["footer"] = random.randint(wlc.sizes_limits["footer"][0], wlc.sizes_limits["footer"][1])
        return dictionary

    def sidebar_first_specific(self):
        return RandomHelper.flip_coin(self.sidebar_first_p)

    def navbar_first_specific(self):
        return RandomHelper.flip_coin(self.navbar_first_p)

    def color_classes_style_specific(self):
        return random.choices(WebLayoutChoices.color_classes_style_choices, self.bg_color_classes_p, k=1)[0]

    def shadow_classes_specific(self):
        return random.choice(WebLayoutChoices.shadow_classes_choices)