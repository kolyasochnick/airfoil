import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button


class AirfoilVisualizer:
    def __init__(self, airfoil):
        self.airfoil = airfoil
        
    
    def show_with_sliders(self):
        upper, lower, mean = self.airfoil.calculate()
        
        x1 = [point[0] for point in upper]
        y1 = [point[1] for point in upper]

        x2 = [point[0] for point in lower]
        y2 = [point[1] for point in lower]

        xm = [point[0] for point in mean]
        ym = [point[1] for point in mean]
        
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # fig.patch.set_facecolor('#181818')
        # ax.set_facecolor('#181818')

        # ax.tick_params(colors='white')
        # ax.xaxis.label.set_color('white')
        # ax.yaxis.label.set_color('white')

        # for spine in ax.spines.values():
        #     spine.set_color('#555555')

        # ax.grid(
        #         color='#444444',
        #         linestyle='--',
        #         alpha=0.5)
        
        plt.subplots_adjust(
                left=0.05,
                right=0.82,
                top=0.95,
                bottom=0.3
                )

        upper_line, = ax.plot(x1, y1, '-', color='red')
        lower_line, = ax.plot(x2, y2, '-', color='blue')
        mean_line, = ax.plot(xm, ym, '--', color='green')

        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(-0.5, 0.5)
        ax.set_aspect('equal', adjustable='box')
        ax.grid()
        
        a_ax = plt.axes([0.92, 0.35, 0.03, 0.5])
        slider_a = Slider(
            a_ax, 
            'a',
            0.0,
            1,
            valinit=self.airfoil.a,
            valstep=0.001,
            orientation='vertical')
        
        b_ax = plt.axes([0.88, 0.35, 0.03, 0.5])
        slider_b = Slider(
            b_ax, 
            'b',
            0.0,
            1,
            valinit=self.airfoil.b,
            valstep=0.001,
                orientation='vertical'
        )
        c_ax = plt.axes([0.84, 0.35, 0.03, 0.5])
        slider_c = Slider(
            c_ax, 
            'c',
            0.0,
            1,
            valinit=self.airfoil.c,
            valstep=0.001,
                orientation='vertical'
        )
        d_ax = plt.axes([0.80, 0.35, 0.03, 0.5])
        slider_d = Slider(
            d_ax, 
            'd',
            0.0,
            1,
            valinit=self.airfoil.d,
            valstep=0.001,
                orientation='vertical'
        )
        e_ax = plt.axes([0.76, 0.35, 0.03, 0.5])
        slider_e = Slider(
            e_ax, 
            'e',
            0.0,
            1,
            valinit=self.airfoil.e,
            valstep=0.001,
                orientation='vertical'
        )
        
        camber_axes = plt.axes([0.2, 0.2, 0.5, 0.03])
        slider_camber = Slider(
            camber_axes,
            'Camber',
            -0.5,
            0.5,
            valinit=self.airfoil.camber,
            valstep=0.01)
        
        Xcamber_axes = plt.axes([0.2, 0.16, 0.5, 0.03])
        slider_Xcamber = Slider(
            Xcamber_axes,
            'Xcamber',
            0.1,
            1.0,
            valinit=self.airfoil.Xcamber,
            valstep=0.1)
        
        thickness_axes = plt.axes([0.2, 0.12, 0.5, 0.03])
        slider_thickness = Slider(
            thickness_axes,
            'thickness',
            0.01,
            0.9,
            valinit=self.airfoil.thickness,
            valstep=0.01)
        
        ax_button = fig.add_axes((0.8, 0.16, 0.1, 0.075))
        safe_button = Button(ax_button, 'SAFE')
        safe_button.on_clicked(self.airfoil.safe)
        
        def update(val):
            self.airfoil.camber = slider_camber.val
            self.airfoil.Xcamber = slider_Xcamber.val
            self.airfoil.thickness = slider_thickness.val
            self.airfoil.a = slider_a.val
            self.airfoil.b = slider_b.val
            self.airfoil.c = slider_c.val
            self.airfoil.d = slider_d.val
            self.airfoil.e = slider_e.val

            upper, lower, mean = self.airfoil.calculate()
            
            upper_line.set_data(
                [point[0] for point in upper],
                [point[1] for point in upper]
            )

            lower_line.set_data(
                [point[0] for point in lower],
                [point[1] for point in lower]
            )

            mean_line.set_data(
                [point[0] for point in mean],
                [point[1] for point in mean]
            )

            fig.canvas.draw_idle()
        
        slider_camber.on_changed(update)
        slider_Xcamber.on_changed(update)
        slider_thickness.on_changed(update)
        slider_a.on_changed(update)
        slider_b.on_changed(update)
        slider_c.on_changed(update)
        slider_d.on_changed(update)
        slider_e.on_changed(update)
        

        plt.show()


if __name__ == '__main__':
    print('vizualization function RUN')
    