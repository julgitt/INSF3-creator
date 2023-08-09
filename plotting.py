"""Function providing type hint support."""
from typing import List, Union
"""Calculate nifs3 for x and y coordinates list."""
from calc import calc_nifs3
"""Module providing data visualisation functions."""
import plotly.express as px
"""Module providing GUI functions."""
import tkinter as tk
"""Module providing graph objects."""
import plotly.graph_objects as go


class Nifs3Plotter:
    """
    Generate and display a NIFS3 plot using Plotly library.

    This function takes lists of X and Y coordinates as input and calculates the NIFS3 plot
    using the `calc_nifs3` function. It then creates a Plotly line plot with the calculated
    NIFS3 data and displays it in a graphical interface.
    """
    def __init__(self, root: tk) -> None:
        self.root: tk = root
        self.root.title("NIFS3 Plot")

        self.points: List[tuple[float, float, int]] = []
        self.canvas: tk.Canvas = tk.Canvas(self.root, width = 600, height = 600, bg = 'white')
        self.canvas.pack()
        self.point_counter: int = 1

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Button-3>", self.on_canvas_right_click)

        self.plot_button: tk.Button = tk.Button(self.root, text = "Plot", command = self.plot_points)
        self.plot_button.pack()

        self.draw_grid()


    def draw_grid(self) -> None:
        """Function drawing grid on the GUI window."""
        for i in range(0, 601, 60):  # Drawing vertical grid lines
            self.canvas.create_line(i, 0, i, 600, fill="lightgray")

        for i in range(0, 601, 60):  # Drawing horizontal grid lines
            self.canvas.create_line(0, i, 600, i, fill="lightgray")


    def on_canvas_click(self, event: tk.Event) -> None:
        """Function binded to the left-click of the mouse event, that creates a new point"""
        x: float
        y: float
        x, y = event.x, event.y
        self.add_point(x, y)
        self.show_point_info(x, y, self.point_counter)
        self.point_counter += 1


    def add_point(self, x: float, y: float) -> None:
        """Function creating a new point"""
        x_coord: float
        y_coord: float
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill = 'red')
        x_coord, y_coord = self._to_data_coordinates(x, y)
        self.points.append((x_coord, y_coord, self.point_counter))


    def on_canvas_right_click(self, event: tk.Event) -> None:
        """Function binded to the right-click of the mouse event, that deletes point"""
        x: float
        y: float
        x, y = event.x, event.y
        self.delete_point(x, y)
        
    def delete_point(self, x: float, y: float) -> None:
        """Function deleting point"""
        to_delete: Union[None, List[tuple[float, float, int]]] = None
        px: float
        py: float
        for point in self.points:
            px, py = self._to_canvas_coordinates(point[0], point[1])
            distance: float = ((px - x) ** 2 + (py - y) ** 2) ** 0.5
            if distance <= 5:  # Check if the distance is within a 5-pixel radius from the clicked point
                to_delete = point
                break

        if to_delete:
            self.canvas.delete("all")
            self.points.remove(to_delete)
            self._redraw_points()


    def _to_canvas_coordinates(self, x: float, y: float) -> tuple[float, float, int]:
        canvas_x: float = x * self.canvas.winfo_width() / 60
        canvas_y: float = self.canvas.winfo_height() - y * self.canvas.winfo_height() / 60
        return canvas_x, canvas_y
    

    def _to_data_coordinates(self, x: float, y: float) -> tuple[float, float, int]:
        x_coord: float = x * 60 / self.canvas.winfo_width()
        y_coord: float = (self.canvas.winfo_height() - y) * 60 / self.canvas.winfo_height()
        return x_coord, y_coord
    

    def _redraw_points(self) -> None:
        self.draw_grid()
        px: float
        py: float
        for point in self.points:
            px, py = self._to_canvas_coordinates(point[0], point[1])
            self.show_point_info(px, py, point[2])
            self.canvas.create_oval(px - 5, py - 5, px + 5, py + 5, fill='red')

    def show_point_info(self, x: float, y: float, point_order: int) -> None:
        """Function preparing the point info to show on the GUI"""
        x_coord, y_coord = self._to_data_coordinates(x, y)
        text: str = f"{point_order:d} : ({x_coord:.2f}, {y_coord:.2f})"
        self.canvas.create_text(x, y - 15, text=text, font=("Helvetica", 10), fill="black")


    def plot_points(self) -> None:
        """Function preparing the points and displaying nifs3 plot"""
        if len(self.points) < 2:
            return
        x_arr: List[float] = [point_info[0] for point_info in self.points]
        y_arr: List[float] = [point_info[1] for point_info in self.points]
        self._display_nifs3_plot(x_arr, y_arr)
    

    def _display_nifs3_plot(self, x: List[float], y: List[float]) -> None:
        """Function creating and displaying nifs3 plot"""
        s_x: float
        s_y: float
        s_x, s_y = calc_nifs3(x, y)
        nifs_plot = px.line(x=s_x, y=s_y, line_shape='linear', labels={'x': 'X Coordinate', 'y': 'Y Coordinate'})
        nifs_plot.update_layout(height=600, width=600, template='plotly_white')
        nifs_plot.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = Nifs3Plotter(root)
    root.mainloop()