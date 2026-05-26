import graphics.drawing as drawing
import graphics.robot_drawings as robot_drawings
import graphics.huds as huds
import robot_components.robots as robots
import files.files_reader as filesr


class Layer:

    def __init__(self):
        """
        Constructor for superclass layer
        """
        self.drawing = drawing.Drawing()
        self.is_drawing = False
        self.hud = None
        self.robot = None
        self.robot_drawing: robot_drawings.RobotDrawing = None
        self._zoom_percentage()
        self.is_drawing = False
        self.is_board = False

        self.rdr = filesr.RobotDataReader()

    def execute(self):
        """
        Executes the code, showing what the robot will do on the canvas
        """
        self._drawing_config()
        self.robot_drawing.draw()
        self.is_drawing = True

    def stop(self):
        """
        Stops all the executing code and clears the canvas
        """
        self.drawing.empty_drawing()
        self.hud.reboot()
        self.is_drawing = False

    def zoom_in(self):
        """
        Broadens the drawing
        """
        self.drawing.zoom_in()
        self._zoom_config()

    def zoom_out(self):
        """
        Unbroads the drawing
        """
        self.drawing.zoom_out()
        self._zoom_config()

    def move(self, using_keys, move_WASD):
        """
        Moves the robot that is being used
        Arguments:
            using_keys: specifies keys are being used for movement (True)
            or not (False)
            move_WASD: a map that specifies if any of the keys WASD is being
            pressed
        """
        pass

    def set_canvas(self, canvas, hud_canvas):
        """
        Sets the canvas that the drawing and will use
        Arguments:
            canvas: the canvas of the drawing
            hud_canvas: the canvas of the hud
        """
        self.drawing.set_canvas(canvas)
        self.drawing.set_size(self.robot_drawing.drawing_width,
                              self.robot_drawing.drawing_height)
        self.hud.set_canvas(hud_canvas)

    def _zoom_config(self):
        """
        Configures the zoom in case when it changes
        """
        self._zoom_percentage()
        if self.is_drawing:
            self._zoom_redraw()

    def _zoom_redraw(self):
        """
        Once the zoom changes, use this method for redrawing everything
        up to scale
        """
        self.drawing.delete_zoomables()
        self._draw_before_robot()
        self.robot_drawing.draw()
        self._draw_after_robot()

    def _draw_before_robot(self):
        pass

    def _draw_after_robot(self):
        pass

    def _zoom_percentage(self):
        """
        Updates the percentage of zoom that is being used currently
        """
        self.zoom_percent = self.drawing.zoom_percentage()

    def _drawing_config(self):
        """
        Method used to configure the drawing before executing
        """
        self.drawing.empty_drawing()

    def delete_elements(self):
        self.drawing.components.clear()
        self.drawing.empty_drawing()
        self.robot.reset()
        self.robot_drawing.draw()
        self.drawing.draw_buttons(self.robot, 500.0, 500.0)
        self.robot.board.pines = []


class MobileRobotLayer(Layer):

    def __init__(self, n_light_sens):
        """
        Constructor for MobileRobotLayer
        Arguments:
            n_light_sens: the number of light sensors
        """
        super().__init__()
        self.hud = huds.MobileHUD()
        self.robot_data = self.rdr.parse_robot(n_light_sens - 2)
        self.robot = robots.MobileRobot(n_light_sens, self.robot_data)
        self.robot_drawing = robot_drawings.MobileRobotDrawing(
            self.drawing, n_light_sens)

        self.n_sens = n_light_sens

        self.is_rotating = False
        self.is_moving = False
        self.circuit = None
        self.obstacle = None

    def move(self, using_keys, move_WASD):
        """
        Move method of the layer. Moves the robot and rotates it
        """
        v = 0  # Velocity
        da = 0  # Angle
        print(f"El angulo es: {da}, y la velocidad es de: {v}")

        if using_keys:
            v, da = self.__move_keys(move_WASD)
        else:
            v, da = self.__move_code()

        future_p = self.robot_drawing.predict_movement(v)
        if (
                v == 0
                or future_p[0] <= self.robot_drawing.width / 2
                or future_p[0] >= self.robot_drawing.drawing_width - self.robot_drawing.width / 2
                or future_p[1] <= self.robot_drawing.height / 2
                or future_p[1] >= self.robot_drawing.drawing_height - self.robot_drawing.height / 2
                or self.__check_obstacle_collision(future_p[0], future_p[1])
        ):
            v = 0
            self.is_moving = False
        # Move or rotate
        if not self.is_rotating:
            self.robot_drawing.move(v)
        if not self.is_moving:
            self.robot_drawing.change_angle(da)
        self.__hud_velocity()

        # Overlapping check
        if self.circuit is not None:
            self.__check_circuit_overlap()
        if self.obstacle is not None:
            self.__detect_obstacle()

    def set_circuit(self, circuit_opt):
        """
        Changes the circuit
        Arguments:
            circuit_opt: the number of the chosen circuit
        """
        circuit_name = self.__parse_circuit_opt(circuit_opt)
        map_tuple = self.rdr.parse_circuit(circuit_name)
        straights = map_tuple[0]
        obstacles = map_tuple[1]
        self.circuit = robot_drawings.Circuit(straights, self.drawing)
        self.obstacle = None
        if len(obstacles) > 0:
            self.obstacle = robot_drawings.Obstacle(obstacles[0], self.drawing)
        self.reset_robot()

    def reset_robot(self):
        """
        Resets the robot
        """
        self.hud = huds.MobileHUD()
        self.robot = robots.MobileRobot(self.n_sens, self.robot_data)
        self.robot_drawing = robot_drawings.MobileRobotDrawing(
            self.drawing, self.n_sens)

    def __move_keys(self, movement):
        """
        Moves the robot using WASD
        Arguments:
            movement: contains the information about the pressing
            of the keys
        """
        v = 0
        da = 0
        if not self.is_rotating:
            if movement["w"] or movement["W"]:
                v = -20
            if movement["s"] or movement["S"]:
                v = 20
            if v != 0:
                self.is_moving = True
            else:
                self.is_moving = False
        if not self.is_moving:
            if movement["a"] or movement["A"]:
                da = 5
            if movement["d"] or movement["D"]:
                da = -5
            if da != 0:
                self.is_rotating = True
            else:
                self.is_rotating = False
        return v, da

    def __move_code(self):
        """
        Moves the robot using the programmed instructions
        """
        v = 0
        da = 0
        # self.robot.servo_left.value = 0
        # self.robot.servo_right.value = 0
        v_i = int((self.robot.servo_left.get_value() - 90) / 10)
        v_r = int((self.robot.servo_right.get_value() - 90) / 10)
        rotates = False
        if v_i >= 0 and v_r >= 0:
            if v_i != 0 or v_r != 0:
                da = 5
                rotates = True
        if v_i <= 0 and v_r <= 0:
            if v_i != 0 or v_r != 0:
                da = -5
                rotates = True
        if abs(v_i) == abs(v_r) and not rotates:
            if v_i > 0:
                v = v_i * 2
            if v_i < 0:
                v = v_i * 2
        if v != 0:
            self.is_moving = True
        else:
            self.is_moving = False
        if da != 0:
            self.is_rotating = True
        else:
            self.is_rotating = False
        return v, da

    def __parse_circuit_opt(self, circuit_opt):
        """
        Parses the option chosen for the circuit
        Arguments:
            circuit_opt: the number which specifies the option
        Returns:
            A string with the corresponding name
        """
        if circuit_opt == 0:
            return "circuit"
        elif circuit_opt == 1:
            return "labyrinth"
        elif circuit_opt == 2:
            return "straight"
        elif circuit_opt == 3:
            return "obstacle"
        elif circuit_opt == 4:
            return "straight and obstacle"
        elif circuit_opt == 5:
            return "node circuit"
        return "circuit"

    def _drawing_config(self):
        """
        Configures the drawing before executing or after
        updating
        """
        super()._drawing_config()
        self.__create_circuit()
        self.__create_obstacle()

    def _draw_before_robot(self):
        """
        Draws before the robot so the z-index is correct
        """
        self.__create_circuit()
        self.__create_obstacle()

    def __create_circuit(self):
        """
        Creates and draws the circuit in the canvas
        """
        if self.circuit is not None:
            self.circuit.create_circuit()

    def __create_obstacle(self):
        """
        Draws the obstacle in the canvas
        """
        if self.obstacle is not None:
            self.obstacle.draw()

    def __check_circuit_overlap(self):
        """
        Checks if the robot is inside or outside of the circuit
        """
        measurements = []
        values = []
        for sens in self.robot_drawing.sensors["light"]:
            x = sens.x
            y = sens.y
            if self.circuit.is_overlapping(x, y):
                sens.dark()
                measurements.append(True)
                values.append(1)
            else:
                sens.light()
                measurements.append(False)
                values.append(0)
        self.robot.set_light_sens_value(values)
        self.robot_drawing.repaint_light_sensors()
        self.hud.set_circuit(measurements)

    def __check_obstacle_collision(self, x, y):
        """
        Checks if the robot collides with the obstacle
        Arguments:
            x: the expected x position
            y: the expected y position
        Returns:
            True if collides, False if else
        """
        if self.obstacle is None:
            return False
        return (
                x + self.robot_drawing.width / 2 >= self.obstacle.x
                and y + self.robot_drawing.height / 2 >= self.obstacle.y
                and x <= self.obstacle.x + (self.obstacle.width + self.robot_drawing.width / 2)
                and y <= self.obstacle.y
                + (self.obstacle.height + self.robot_drawing.height / 2)
        )

    def __detect_obstacle(self):
        """
        Checks for every ultrasound sensor if it detects
        any obstacle in front of it, and then sends the data
        to the hud, so it can be parsed
        """
        dists = []
        dists.append(self.obstacle.calculate_distance(self.robot_drawing.sensors["sound"].x,
                                                      self.robot_drawing.sensors["sound"].y, self.robot_drawing.angle))
        if dists[-1] != -1:
            self.robot_drawing.sensors["sound"].set_detect(True)
            self.robot.sound.value = 1
            self.robot.sound.dist = dists[-1]
        else:
            self.robot_drawing.sensors["sound"].set_detect(False)
            self.robot.sound.value = 0
            self.robot.sound.dist = -1
        self.hud.set_detect_obstacle(dists)

    def __hud_velocity(self):
        """
        Sends the velocity data of the wheels to the hud,
        so it can be parsed
        """
        self.hud.set_wheel([self.robot_drawing.vl, self.robot_drawing.vr])


class LinearActuatorLayer(Layer):

    def __init__(self):
        """
        Constuctor for LinearActuatorLayer
        """
        super().__init__()
        self.hud = huds.ActuatorHUD()
        self.robot_data = self.rdr.parse_robot(3)
        self.robot = robots.LinearActuator(self.robot_data)
        self.robot_drawing = robot_drawings.LinearActuatorDrawing(self.drawing)

    def move(self, using_keys, move_WASD):
        """
        Move method of the layer. Moves the block of the
        linear actuator
        """
        v = 0
        self.robot_drawing.hit = False
        if using_keys:
            v = self.__move_keys(move_WASD)
        else:
            v = self.__move_code()
        self.robot_drawing.move(v)
        self.hud.set_direction(v * 25)
        self.hud.set_pressed(
            [self.robot_drawing.but_left.pressed, self.robot_drawing.but_right.pressed])

    def __move_keys(self, movement):
        """
        Moves the robot using WASD
        Arguments:
            movement: contains the information about the pressing
            of the keys
        """
        v = 0
        if movement["a"] or movement["A"]:
            if self.robot_drawing.block.x > 508:
                v -= 15
            self.__hit_left(v == 0)
        elif movement["d"] or movement["D"]:
            if self.robot_drawing.block.x < 1912:
                v += 15
            self.__hit_right(v == 0)
        return v

    def __move_code(self):
        """
        Moves the robot using the programmed instructions
        """
        v = 0
        v_s = int((self.robot.servo.value - 90) / 10) * -1
        if v_s > 0:
            if self.robot_drawing.block.x < 1912:
                v = v_s * 2
            else:
                self.__hit_right(True)
        if v_s < 0:
            if self.robot_drawing.block.x > 508:
                v = v_s * 2
            else:
                self.__hit_left(True)
        if v != 0:
            self.__hit_left(False)
            self.__hit_right(False)
        return v

    def __hit_left(self, has_hit):
        """
        Establishes the value for the left button
        Arguments:
            has_hit: True if the button has been hit, False
            if else
        """
        if has_hit:
            self.robot_drawing.hit = True
            self.robot.button_left.value = 0
        else:
            self.robot_drawing.hit = False
            self.robot.button_left.value = 1

    def __hit_right(self, has_hit):
        """
        Establishes the value for the right button
        Arguments:
            has_hit: True if the button has been hit, False
            if else
        """
        if has_hit:
            self.robot_drawing.hit = True
            self.robot.button_right.value = 0
        else:
            self.robot_drawing.hit = False
            self.robot.button_right.value = 1


class ArduinoBoardLayer(Layer):
    def __init__(self):
        """
        Constuctor for ArduinoBoard
        """
        super().__init__()
        self.is_board = True
        self.prev_x = 0
        self.prev_y = 0
        self.hud = huds.ArduinoBoardHUD()
        self.robot = robots.ArduinoBoard(self)
        self.robot_drawing = robot_drawings.ArduinoBoardDrawing(
            self.drawing)
        self.drawing.setBoard(self.robot.board)

    def set_canvas(self, canvas, hud_canvas):
        """
        Sets the canvas that the drawing and will use
        Arguments:
            canvas: the canvas of the drawing
            hud_canvas: the canvas of the hud
        """
        self.drawing.set_canvas(canvas)
        self.drawing.set_size(self.robot_drawing.drawing_width,
                              self.robot_drawing.drawing_height)
        self.hud.set_canvas(hud_canvas)
        self.robot_drawing.draw()
        self.drawing.draw_buttons(self.robot, 500.0, 500.0)

    def _zoom_config(self):
        """
        Configures the zoom in case when it changes
        """
        self._zoom_percentage()
        self._zoom_redraw()

    def stop(self):
        """
        Stops all the executing code and clears the canvas
        """
        self.is_drawing = False

    def draw_component(self, x, y):
        if self.hud.drawing is not None:
            element = self.robot.add_component(self.hud.drawing)
            self.drawing.draw_component(element, x, y)
            self.hud.drawing = None
        elif self.hud.draw_wire:
            dibujar = self.drawing.draw_part_wire(x, y)
            # It is needed to the correct work of the wire
            if not dibujar:
                self.hud.draw_wire = False

    def _draw_after_robot(self):
        """Draw the components on the canvas"""
        self.drawing.draw_all_components()
        self.drawing.draw_all_buttons()
        self.drawing.redraw_wire()

    def probe(self, option_gamification, user_code, robot_code):
        return self.drawing.probe(option_gamification, user_code, robot_code,
                                  self.robot, self.get_robot_challenge(option_gamification))

    def show_tutorial(self):
        self.drawing.show_tutorial()

    def show_results(self):
        self.drawing.show_results()

    def show_help(self, option_gamification):
        self.drawing.show_help(option_gamification)

    def get_robot_challenge(self, option_gamification):
        return self.drawing.get_robot_challenge(option_gamification)
