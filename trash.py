            # for app in self.apps:
            #     # self.app is when the user wants to update an app
            #     if name in app and self.app is None:
            #         Message("This name is already being used", "Name already exists").exec_()
            #         is_unique = False

            #     elif path in app and self.app is None:
            #         Message("This path is already being used", "Path already exists").exec_()
            #         is_unique = False

            # if is_unique and not self.app:
            #     for app in self.apps:

            #         if index <= len(self.apps):

            #             if app[3] >= index:
            #                 Model().update('apps', {'sequence': app[3] + 1}, app[0])
            #     Model().save('apps', data)
            #     self.app_window_signal.emit("saved")
            #     self.close()

            # elif self.app is not None:
            #     if self.app[3] != index:
            #         old = self.app[3] - 1
            #         new = index - 1
            #         move_up = True if old > new else False
            #         global array
            #         if move_up:
            #             array = self.apps[new:old]
            #         elif not move_up:
            #             array = self.apps[old+1:new+1]
            #         for app in array:
            #             app = list(app)
            #             if move_up:
            #                 Model().update('apps', {'sequence': app[3] + 1}, app[0])
            #             elif not move_up:
            #                 Model().update('apps', {'sequence': app[3] - 1}, app[0])
            #     Model().update('apps', data, self.app[0])
            #     self.app_window_signal.emit("updated")
            #     self.close()