from wise.networks.network import Network


class MLP(Network):
    """
    Generic class for creating multi-layer perceptrons from individual
    layers.
    """

    def __init__(self, name, session, input_shape, layer_constructors_generator,
            layer_shapes, input_node=None, save_location=None):
        """
        String -> tf.Session -> [Int] -> (Int ->
            [String -> tf.Session -> [Int] -> [Int] -> tf.Tensor? -> String? -> Layer])
             -> [[Int]] -> tf.Tensor? -> String? -> MLP
        Create a MLP from a number of standard parameters, as well as a function
        which, given the number of layers the network will have, produces a list
        of layer generators.
        """
        super().__init__(name, session, save_location)

        self.input_shape = input_shape
        self.layer_shapes = layer_shapes
        self.output_shape = output_shape

        self.layer_constructors_generator = layer_constructors_generator

        self.input_node = input_node
        self.layers = None
        self.output_node = None

    def _initialise(self):
        """
        () -> ()
        Initialise the network's layers.
        """
        full_layers = [self.input_shape] + self.layer_shapes + [self.output_shape]
        layer_params = zip(full_layers[:-1], full_layers[1:])
        constructors = self.layer_constructors_generator(len(self.layer_shapes) + 1)
        
        self.layers = []
        previous_layer_output = self.get_input_node()
        for constructor, (in_shape, out_shape) in zip(constructors, layer_params):
            self.layers.append(constructor(
                self.extend_name('layer_{}'.format(len(self.layers))),
                self.get_session(), in_shape, out_shape, previous_layer_output))
            previous_layer_output = self.layers[-1].get_output_node()
        self.output_node = previous_layer_output

    def get_input_node(self):
        """
        () -> tf.Tensor
        """
        return self.input_node

    def get_output_node(self):
        """
        () -> tf.Tensor
        """
        return self.output_node

    def get_variables():
        """
        () -> [tf.Variable]
        """
        outputs = []
        for layer in self.layers:
            outputs += layer.get_variables()
        return outputs
