import numpy as np
import gym

from gym import spaces
from gym.utils import seeding


class BernoulliBanditEnv(gym.Env):
    """Multi-armed bandit problems with Bernoulli observations, as described
    in [1].

    At each time step, the agent pulls one of the `k` possible arms (actions),
    say `i`, and receives a reward sampled from a Bernoulli distribution with
    parameter `p_i`. The multi-armed bandit tasks are generated by sampling
    the parameters `p_i` from the uniform distribution on [0, 1].

    [1] Yan Duan, John Schulman, Xi Chen, Peter L. Bartlett, Ilya Sutskever,
        Pieter Abbeel, "RL2: Fast Reinforcement Learning via Slow Reinforcement
        Learning", 2016 (https://arxiv.org/abs/1611.02779)
    """

    def __init__(self, k, task={}):
        super(BernoulliBanditEnv, self).__init__()
        self.k = k

        self.action_space = spaces.Discrete(self.k)
        self.observation_space = spaces.Box(low=0, high=0, shape=(1,), dtype=np.float32)

        self._task = task
        self._means = task.get("mean", np.full((k,), 0.5, dtype=np.float32))
        self.seed()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def sample_tasks(self, num_tasks):
        means = self.np_random.rand(num_tasks, self.k)
        tasks = [{"mean": mean} for mean in means]
        return tasks

    def reset_task(self, task):
        self._task = task
        self._means = task["mean"]

    def reset(self):
        return np.zeros(1, dtype=np.float32)

    def step(self, action):
        assert self.action_space.contains(action)
        mean = self._means[action]
        reward = self.np_random.binomial(1, mean)
        observation = np.zeros(1, dtype=np.float32)

        return observation, reward, True, {"task": self._task}


class GaussianBanditEnv(gym.Env):
    """Multi-armed problems with Gaussian observations.

    At each time step, the agent pulls one of the `k` possible arms (actions),
    say `i`, and receives a reward sampled from a Normal distribution with
    mean `p_i` and standard deviation `std` (fixed across all tasks). The
    multi-armed bandit tasks are generated by sampling the parameters `p_i`
    from the uniform distribution on [0, 1].
    """

    def __init__(self, k, std=1.0, task={}):
        super(GaussianBanditEnv, self).__init__()
        self.k = k
        self.std = std

        self.action_space = spaces.Discrete(self.k)
        self.observation_space = spaces.Box(low=0, high=0, shape=(1,), dtype=np.float32)

        self._task = task
        self._means = task.get("mean", np.full((k,), 0.5, dtype=np.float32))
        self.seed()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def sample_tasks(self, num_tasks):
        means = self.np_random.rand(num_tasks, self.k)
        tasks = [{"mean": mean} for mean in means]
        return tasks

    def reset_task(self, task):
        self._task = task
        self._means = task["mean"]

    def reset(self):
        return np.zeros(1, dtype=np.float32)

    def step(self, action):
        assert self.action_space.contains(action)
        mean = self._means[action]
        reward = self.np_random.normal(mean, self.std)
        observation = np.zeros(1, dtype=np.float32)

        return observation, reward, True, {"task": self._task}
