"""
Author: Fredy Ramirez <https;//formateli.com>
License: GNU GPLv3
"""
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk


class OnOffButton(ttk.Checkbutton):
    """
    A simple On/Off button.
    """

    _images = None

    def __init__(self, master=None, **kwargs):
        """
        Create an OnOffButton.

        :param master: master widget
        :type master: widget
        :command: A function to be called whenever the state of this onoffbutton changes.
        :type command: callback function.
	    :param onvalue: Value returned by onoffbutton when it is 'on'. Default 'on'.
        :type onvalue: It depends of variable type.
	    :param offvalue: Value returned by onoffbutton when it is 'off'. Default 'off'.
        :type offvalue: It depends of variable type.
	    :param variable: A control variable that tracks the current state of the onoffbutton.
        :                It can be IntVar, BooleanVar or StringVar. Default StringVar.
        :type variable: Tk control variable.
        :style: The ttk style to be used in rendering onoffbutton. Default 'OnOffButton'.
        :type style: str.
        """
        OnOffButton._setup_style()

        kwargs['variable'], kwargs['onvalue'], kwargs['offvalue'] = \
                self._validate_variable(kwargs.pop('variable', None),
                                        kwargs.pop('onvalue', 'on'),
                                        kwargs.pop('offvalue', 'off'))
        kwargs['style'] = kwargs.pop('style', 'OnOffButton')
        super(OnOffButton, self).__init__(master, class_='OnOffButton', **kwargs)
        self._variable = kwargs['variable']
        self._variable.set(kwargs['offvalue'])

    def get(self):
        """
        Get current state value of onoffbutton.
        Returns 'onvalue' or 'offvalue'.
        """
        return self._variable.get()

    def set(self, value):
        """
        Set the state value for onoffbutton.

        :param value: Value to set. It must be 'onvalue' or 'offvalue'.
        """
        self._variable.set(value)

    def _validate_variable(self, variable, onvalue, offvalue):
        if variable is None:
            variable = tk.StringVar()
        if isinstance(variable, tk.IntVar):
            onvalue = self._validate_int(onvalue, 1)
            offvalue = self._validate_int(offvalue, 0)
        if isinstance(variable, tk.BooleanVar):
            onvalue = True
            offvalue = False
        if isinstance(variable, tk.StringVar):
            onvalue = str(onvalue)
            offvalue = str(offvalue)
        if onvalue == offvalue:
            raise ValueError('onvalue and offvalue must be diferent.')
        return variable, onvalue, offvalue

    def _validate_int(self, val, default):
        if not isinstance(val, int):
            return default
        return val

    @classmethod
    def _setup_style(cls):
        """
        Setups the style for the OnOffButton.
        :param bg:
        :param disabledbg:
        """
        if OnOffButton._images is not None:
            return

        style = ttk.Style()
        dummy_widget = ttk.Checkbutton()

        OnOffButton._images = (  # Must be on cls to keep reference
            tk.PhotoImage("img_switch", data="""
                iVBORw0KGgoAAAANSUhEUgAAADQAAAAYCAMAAACCyC6UAAADAFBMVEUAAAD////Q
                2ePR0eTM1ebO1ubP1eTQ1eXR1ubP1uXQ1+bQ1+bP1ufP1ufQ1+jO1eXO1+bO1efO
                1ebP1ubQ1ubP1ubQ1ubO1ufP1eXP1ubP1ubP1ubQ1+bO1ubP1ubP1ufP1ubP1ubP
                1ubQ1ebP1ufP1ubP1ebP1ubP1ubW3OrP1ubW3OrP1ubP1ubP1ubQ1ubW2+nX3OrP
                1ubP1ubc4u3P1ubb4ezd4u3P1uaKkJ2LkJ6LkZ+Mkp+kqrimq7qmrLqnrbynrr2o
                rrypr72psL+qsL2qsL6rssDO1eXP1ubW3Ora4Ozb4ezc4e3s7vXs7/Xz9Pnz9fn3
                +Pv3+fv4+fv7/P38/P38/f79/f7///9aWlpbW1tcXFxdXV1eXl5fX19gYGBhYWFi
                YmJjY2NkZGRlZWVmZmZnZ2doaGhpaWlqampra2tsbGxtbW1ubm5vb29wcHBxcXFy
                cnJzc3N0dHR1dXV2dnZ3d3d4eHh5eXl6enp7e3t8fHx9fX1+fn5/f3+AgICBgYGC
                goKDg4OEhISFhYWGhoaHh4eIiIiJiYmKioqLi4uMjIyNjY2Ojo6Pj4+QkJCRkZGS
                kpKTk5OUlJSVlZWWlpaXl5eYmJiZmZmampqbm5ucnJydnZ2enp6fn5+goKChoaGi
                oqKjo6OkpKSlpaWmpqanp6eoqKipqamqqqqrq6usrKytra2urq6vr6+wsLCxsbGy
                srKzs7O0tLS1tbW2tra3t7e4uLi5ubm6urq7u7u8vLy9vb2+vr6/v7/AwMDBwcHC
                wsLDw8PExMTFxcXGxsbHx8fIyMjJycnKysrLy8vMzMzNzc3Ozs7Pz8/Q0NDR0dHS
                0tLT09PU1NTV1dXW1tbX19fY2NjZ2dna2trb29vc3Nzd3d3e3t7f39/g4ODh4eHi
                4uLj4+Pk5OTl5eXm5ubn5+fo6Ojp6enq6urr6+vs7Ozt7e3u7u7v7+/w8PDx8fHy
                8vLz8/P09PT19fX29vb39/f4+Pj5+fn6+vr7+/v8/Pz9/f3+/v7////J3IgwAAAA
                OXRSTlMAARscHh8wMTJFRkdKS0xOU1Rub3GanJ2foLW2t8LFxtPU1dfb3N3r7O/w
                8PHy9Pf4+Pr7+/z8/P2pOdQBAAABJUlEQVR4nL3U2VbCMBAG4FZAXFBAERAXFMEd
                3JeobBahETC2IKbv/yJODUjb9IzChf/VXPQ7SSeZKMp/J5TY3C9RJKXCRiLkIsH1
                O9bnvMe6mKNX6cDYLJ8Y1jDGK8oOl0YmejuwfjJoo+o+LszchcOAwtc6C9tGzRqW
                KwaKaFYFtNi1PMG7QecBpZkXMfnDxwalrQf9u04C2ut7UU9GdaI1SUXUu4CK3Iu4
                jPQaIeVhXQR0KqFPnx9pEVIVu6PHgHLS9kzZNEntmWii3gGUkhrx5tMITddfnsRS
                a4AWpJZ3fLbniN1ydet9osPdtg9XCZ9/OM1v12h28gt7Extd88jRX0fjIDIeqEDq
                mpmcmwzvwWVyxj27q5k8Pu75zEpw6tdk2nwBcgYKibbxIuoAAAAASUVORK5CYII=
                """, master=dummy_widget),

            tk.PhotoImage("img_switch_active", data="""
                iVBORw0KGgoAAAANSUhEUgAAADQAAAAYCAMAAACCyC6UAAADAFBMVEUAAAAA//9V
                l+NSkuRVkeZSlN5QleRTkuBSlOBRlOFUleJTk+JTlONSluBRlOFSk+JTk+NSleFR
                lOFTk+FRleJTk+FSleJRlOJSlOJRlOJSlOFTleJSlOJRleJSlONSlOFSk+JSlOJR
                lOJSlONSlOJSlOJSlOJSlOJSlOJspOZtpOZSlOJRlOJSlOFSlOJSlOJro+ZSlOJS
                lOJ/sOuBsep8rel8rulSlOJZmONZmeNloOVmoOVoouZpouZqo+ZrpOZspOZ3q+h7
                rel7rul8rul/sOqAseqBseqLt+yixe+pyvGqyvGuzfK51PO61PO61fS71fS81fTS
                4/fT5PjU5PjU5fjV5fjj7vrk7vrl7/vm7/vr8vzs8/zx9/3z9/3z+P31+f33+v74
                +v78/f////9lZWVmZmZnZ2doaGhpaWlqampra2tsbGxtbW1ubm5vb29wcHBxcXFy
                cnJzc3N0dHR1dXV2dnZ3d3d4eHh5eXl6enp7e3t8fHx9fX1+fn5/f3+AgICBgYGC
                goKDg4OEhISFhYWGhoaHh4eIiIiJiYmKioqLi4uMjIyNjY2Ojo6Pj4+QkJCRkZGS
                kpKTk5OUlJSVlZWWlpaXl5eYmJiZmZmampqbm5ucnJydnZ2enp6fn5+goKChoaGi
                oqKjo6OkpKSlpaWmpqanp6eoqKipqamqqqqrq6usrKytra2urq6vr6+wsLCxsbGy
                srKzs7O0tLS1tbW2tra3t7e4uLi5ubm6urq7u7u8vLy9vb2+vr6/v7/AwMDBwcHC
                wsLDw8PExMTFxcXGxsbHx8fIyMjJycnKysrLy8vMzMzNzc3Ozs7Pz8/Q0NDR0dHS
                0tLT09PU1NTV1dXW1tbX19fY2NjZ2dna2trb29vc3Nzd3d3e3t7f39/g4ODh4eHi
                4uLj4+Pk5OTl5eXm5ubn5+fo6Ojp6enq6urr6+vs7Ozt7e3u7u7v7+/w8PDx8fHy
                8vLz8/P09PT19fX29vb39/f4+Pj5+fn6+vr7+/v8/Pz9/f3+/v7///+uaILKAAAA
                N3RSTlMAARscHh8wMTJFRkdKS0xOU1Rub3GanJ2foLW2t8LFxtPU1dfb3N3s7e7v
                8PHy9Pf4+vv7/P39KwCFLAAAASxJREFUeJy91GdTwkAQBuBEQCwoFgTEAirYQaxn
                74ggRgQhYAmG7P//DV6EkMvlZsfhg+/X3Wfu5rIbSfrv+ELzqxmCJJOaC/kcxDu7
                hwGSLzfb7cbLQdRjm/F1lFzXoZva5phlgvgx9y3opXU02TFDO/g5jAHQsn7TyHHU
                kCo4Uo/LFI0yDSdnLpMHLrlhiqJ2w3Hl44JHrzxSwhStMAY+L3nU5FFjiaK0WTp9
                L4oN0XmkpynaNks3BpSExo2+tyha/q09GiA07uupCYoineITGCJDyjx6nqFopFst
                3IoMeRA+ubwgbO6l4jS1RfPjSn58jM6/WKNlB/80sHcaYw4nrDEPrKHq6s0y1Y2A
                vVCeyC7Kcoqq66qyHx5w7u50LImvezI25e37b9JvfgAjU++Y681BdAAAAABJRU5E
                rkJggg==
                """, master=dummy_widget),

            tk.PhotoImage("img_switch_active_insensitive", data="""
                iVBORw0KGgoAAAANSUhEUgAAADQAAAAYCAMAAACCyC6UAAADAFBMVEUAAAAA//9V
                md1Vme5Qj+9LluFOk+tVjuNVl+NRlN1XmuRVluVRleBPkuFTlOFTkONTluNRleFU
                kuJSlOJRk+FQlOFSleJRlOJSleNSlOBSlONRlOBTleNSk+FRk+JRleJRlONSleNR
                leNSlOFSlORSk+JSleJrpOZtpehRk+JRleJSlOBSlOJRlOFro+dSleNRlOGAsOuB
                set9rOl9rulSlOJZl+RZmeRkoOZmoOZoouZqouZrpOZ2q+d8rel8r+mAsemBsemK
                tu2ixe+pyvCvzvK60/K61fS81fTR5PjT5PjT5vjV5vjk7/rm7/vr8vvt8vvw+P3y
                +P32+v34+v37/f////9XV1dYWFhZWVlaWlpbW1tcXFxdXV1eXl5fX19gYGBhYWFi
                YmJjY2NkZGRlZWVmZmZnZ2doaGhpaWlqampra2tsbGxtbW1ubm5vb29wcHBxcXFy
                cnJzc3N0dHR1dXV2dnZ3d3d4eHh5eXl6enp7e3t8fHx9fX1+fn5/f3+AgICBgYGC
                goKDg4OEhISFhYWGhoaHh4eIiIiJiYmKioqLi4uMjIyNjY2Ojo6Pj4+QkJCRkZGS
                kpKTk5OUlJSVlZWWlpaXl5eYmJiZmZmampqbm5ucnJydnZ2enp6fn5+goKChoaGi
                oqKjo6OkpKSlpaWmpqanp6eoqKipqamqqqqrq6usrKytra2urq6vr6+wsLCxsbGy
                srKzs7O0tLS1tbW2tra3t7e4uLi5ubm6urq7u7u8vLy9vb2+vr6/v7/AwMDBwcHC
                wsLDw8PExMTFxcXGxsbHx8fIyMjJycnKysrLy8vMzMzNzc3Ozs7Pz8/Q0NDR0dHS
                0tLT09PU1NTV1dXW1tbX19fY2NjZ2dna2trb29vc3Nzd3d3e3t7f39/g4ODh4eHi
                4uLj4+Pk5OTl5eXm5ubn5+fo6Ojp6enq6urr6+vs7Ozt7e3u7u7v7+/w8PDx8fHy
                8vLz8/P09PT19fX29vb39/f4+Pj5+fn6+vr7+/v8/Pz9/f3+/v7///+yPa/OAAAA
                V3RSTlMAAQ8PEBEaGxsmJicpKisuLjw9PlVWV1hjZGRrbG10dHV2eHl5goKDg4SE
                hYaIiImKioqLi4yMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIzAksdu
                AAABH0lEQVR4nL3U21LCQAwG4K2AeABRoIgKKqiogHhcj6hFoHJq1dru+z+KqUBp
                t5nMyIX/bfLNdnaTMvbfiWW2D+ucSP1gKxMLkOjmBQV4q2fatvF+lYvMTLJCkuZI
                TDI8SUzNGn3MqyW8WDfrY7N0Rp/jM6AacdcoRdLwgQhkVFQArfoa7h5CpiWkaMuA
                crOG2/7Hk4x6MtJVQCWfEZ8hZMrI2ANUc0v3Zgc33JaRXQNUdUvPjuiiJoy+TwHt
                /9beHIEa5PN2AanjYkc4mEEuIgtoZVJtv2CGa+iVKztos5d+0AwL7uOyOD1Gj19+
                YzUW/z6w16npmCeOSNX0xm9w7K0GYxH1nGSabsAS6pfqQnB30/kyve7l/EZ0/t/J
                nPkB7ijb9HXezlAAAAAASUVORK5CYII=
                """, master=dummy_widget),

            tk.PhotoImage("img_switch_insensitive", data="""
                iVBORw0KGgoAAAANSUhEUgAAADQAAAAYCAMAAACCyC6UAAADAFBMVEUAAAD////M
                3d3d3e7P3+/S0uHO2OvQ2ePZ2ezQ1+TQ1+vR2OXN0+bN2ubO1efQ1eHN0+PN0+nQ
                2ebN1ebS1ubP1eTQ1eTQ1efQ1ujO1uXR1uXP1ubR2ejN1OXQ1+fO1eXP1eXP1+fP
                1uXP1ufQ1+jP1+bQ1eXO1ubW3OrP1ebR1ubV3OrP1ebP1+bO1uXW2+rY2+rP1ufP
                1uXR1ufc4e3e4e3P1eWKkJ2KkJ6Kkp6Mkp6kqbimq7qorbyor7yor72pr72psb2p
                sb+rs7/O1ebQ1ebV3Onb4O3b4u3c4u3t7/by9Pry9vr4+Pv4+vv7+/37/f39/f3/
                //9TU1NUVFRVVVVWVlZXV1dYWFhZWVlaWlpbW1tcXFxdXV1eXl5fX19gYGBhYWFi
                YmJjY2NkZGRlZWVmZmZnZ2doaGhpaWlqampra2tsbGxtbW1ubm5vb29wcHBxcXFy
                cnJzc3N0dHR1dXV2dnZ3d3d4eHh5eXl6enp7e3t8fHx9fX1+fn5/f3+AgICBgYGC
                goKDg4OEhISFhYWGhoaHh4eIiIiJiYmKioqLi4uMjIyNjY2Ojo6Pj4+QkJCRkZGS
                kpKTk5OUlJSVlZWWlpaXl5eYmJiZmZmampqbm5ucnJydnZ2enp6fn5+goKChoaGi
                oqKjo6OkpKSlpaWmpqanp6eoqKipqamqqqqrq6usrKytra2urq6vr6+wsLCxsbGy
                srKzs7O0tLS1tbW2tra3t7e4uLi5ubm6urq7u7u8vLy9vb2+vr6/v7/AwMDBwcHC
                wsLDw8PExMTFxcXGxsbHx8fIyMjJycnKysrLy8vMzMzNzc3Ozs7Pz8/Q0NDR0dHS
                0tLT09PU1NTV1dXW1tbX19fY2NjZ2dna2trb29vc3Nzd3d3e3t7f39/g4ODh4eHi
                4uLj4+Pk5OTl5eXm5ubn5+fo6Ojp6enq6urr6+vs7Ozt7e3u7u7v7+/w8PDx8fHy
                8vLz8/P09PT19fX29vb39/f4+Pj5+fn6+vr7+/v8/Pz9/f3+/v7////QOFaRAAAA
                U3RSTlMAAQ8PEBEaGxsmJicpKSorLi48PT5VVlZXWGNkZGtsbXR0dXZ4eYGCg4SE
                hIWGiIiIiYqKioqLjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjDj87KcAAAEd
                SURBVHicvdTZVsIwEAbgVkBcUBYREBcEWRVc0biAtNKAhLaYvv/DOCUgtOHMoVz4
                X81Fv5N0komi/Hci6bNKiyJpVU7TEQ8Jnzwzm3ObjTBHH3OhhTm8MZ1ZzAHKagdz
                E29PnL9Mhqh6SQqzc79kQOFr3UZdoxZMxxMTRbSgAtofOb7g3aC7gHLMj5j84dsX
                pf1XY1pnAF3ZfmTLqEc0nXREXQTU5H7EZWR0CfmY1U1A1xL6WfEjfUI6Yne0Aagk
                bc+SjU66n0QT9SWg7FqN0AxDfxdLHQPak1r+vWJ7S3Fbrp6PAx3uhXu4SvQu0DXa
                Dn5hnxLzax6rrzsa1dhioELZNrM4txjeg4fMlnd2j/JlfNzL+VR449dk0/wCFTr6
                UPmZVCwAAAAASUVORK5CYII=
                """, master=dummy_widget),
        )

        for seq in dummy_widget.bind_class("TCheckbutton"):
            dummy_widget.bind_class("OnOffButton", seq,
                            dummy_widget.bind_class("TCheckbutton", seq), True)

        style.element_create(
                'Switch.switch', 'image', 'img_switch',
                ('disabled', 'selected', 'img_switch_active_insensitive'),
                ('selected', 'img_switch_active'),
                ('disabled', 'img_switch_insensitive'),
                width=52,
                sticky='w'
            )

        style.layout('OnOffButton',
            [
                (
                    'Switch.padding',
                    {
                        'sticky': 'nswe',
                        'children': [
                            (
                                'Switch.switch',
                                {
                                    'side': 'left', 'sticky': ''
                                }
                            ),
                            (
                                'Switch.focus',
                                {
                                    'side': 'left', 'sticky': 'w',
                                    'children': [
                                        (
                                            'Switch.label',
                                            {
                                                'sticky': 'nswe'
                                            }
                                        )
                                    ]
                                }
                            )
                        ]
                    }
                )
            ]
        )

        style.configure('OnOffButton',
                        **style.configure('TCheckbutton').copy())
