

class Policy(object):
    def __init__(self,
                 name='policy',
                 hidden_sizes=(32, 32),
                 activation='tanh',
                 **kwargs
                 ):
        """
        Also provides functions for executing and updating policy parameters
        A container for storing the current pre and post update policies
        Args:

        """
        self.name = name
        self.hidden_sizes = hidden_sizes
        self.activation = activation

        self._env_spec = None
        self.init_policy = None
        self.policy_params = None

    def build_graph(self, env_spec, **kwargs):
        raise NotImplementedError

    def get_action(self, observation):
        """
        Runs a single observation through the specified policy
        Args:
            observation (array) : single observation
            policy_params (params) :
        Returns:
            (array) : array of arrays of actions for each env
        """
        # TODO: Call get_actions
        raise NotImplementedError

    def get_actions(self, observations):
        """
        Runs each set of observations through each task specific policy
        Args:
            observations (array) : array of arrays of observations generated by each task and env
        Returns:
            (array) : array of arrays of actions for each env
        """
        raise NotImplementedError

    def reset(self, dones=None):
        pass

    def log_diagnostics(self, paths):
        """
        Log extra information per iteration based on the collected paths
        """
        pass

    def load_params(self, policy_params):
        """
        Args:
            policy_params (array): array of policy parameters for each task
        """
        raise NotImplementedError

    @property
    def distribution(self):
        """
        Returns:
            (Distribution) : this policy's distribution
        """
        raise NotImplementedError

    def dist_info_sym(self, obs_var, state_info_vars):
        """
        Return the symbolic distribution information about the actions.
        Args:
            obs_var (placeholder) : symbolic variable for observations
            state_info_vars (dict) : a dictionary of placeholders that contains information about the
            state of the policy at the time it received the observation
        Returns:
            (dict) : a dictionary of tf placeholders for the policy output distribution
        """
        raise NotImplementedError

    def dist_info(self, obs, state_infos):
        """
        Args:
            obs (placeholder) : symbolic variable for observations
            state_infos (dict) : a dictionary of placeholders that contains information about the
            state of the policy at the time it received the observation
        Returns:
            (dict) : a dictionary of tf placeholders for the policy output distribution
        """
        raise NotImplementedError


class MetaPolicy(Policy):
    def build_graph(self, env_spec, num_tasks=1):
        raise NotImplementedError

    def switch_to_pre_update(self):
        """
        It switches to the pre-updated policy
        """
        self._pre_update_mode = True

    def get_actions(self, observations):
        if self._pre_update_mode:
            return self._get_pre_update_actions(observations)
        else:
            return self._get_post_update_actions(observations)

    def _get_pre_update_actions(self, observations):
        """
        Args:
            observations (list): List of size meta-batch size with numpy arrays of shape batch_size x obs_dim

        """
        raise NotImplementedError

    def _get_post_update_actions(self, observations):
        """
        Args:
            observations (list): List of size meta-batch size with numpy arrays of shape batch_size x obs_dim

        """
        raise NotImplementedError

    def update_parameters(self, updated_policies_parameters):
        """
        Args:
            updated_policies_parameters (list): List of size meta-batch size. Each contains a dict with the policies
            parameters

        """
        self.policies_parameters = updated_policies_parameters
        self._pre_update_mode = False
        raise NotImplementedError

