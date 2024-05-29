# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.


from __future__ import annotations

from typing import List

from ufo.agents.agent.app_agent import AppAgent
from ufo.config.config import Config
from ufo.prompter.agent_prompter import FollowerAgentPrompter

configs = Config.get_instance().config_data


class FollowerAgent(AppAgent):
    """
    The FollowerAgent class the manager of a FollowedAgent that follows the step-by-step instructions for action execution within an application.
    It is a subclass of the AppAgent, which completes the action execution within the application.
    """

    def __init__(
        self,
        name: str,
        process_name: str,
        app_root_name: str,
        is_visual: bool,
        main_prompt: str,
        example_prompt: str,
        api_prompt: str,
        app_info_prompt: str,
    ):
        """
        Initialize the FollowAgent.
        :param name: The name of the agent.
        :param process_name: The process name of the app.
        :param app_root_name: The root name of the app.
        :param is_visual: The flag indicating whether the agent is visual or not.
        :param main_prompt: The main prompt file path.
        :param example_prompt: The example prompt file path.
        :param api_prompt: The API prompt file path.
        :param app_info_prompt: The app information prompt file path.
        """
        super().__init__(
            name=name,
            process_name=process_name,
            app_root_name=app_root_name,
            is_visual=is_visual,
            main_prompt=main_prompt,
            example_prompt=example_prompt,
            api_prompt=api_prompt,
            skip_prompter=True,
        )

        self.prompter = self.get_prompter(
            is_visual,
            main_prompt,
            example_prompt,
            api_prompt,
            app_info_prompt,
            app_root_name,
        )

    def get_prompter(
        self,
        is_visual: str,
        main_prompt: str,
        example_prompt: str,
        api_prompt: str,
        app_info_prompt: str,
        app_root_name: str = "",
    ) -> FollowerAgentPrompter:
        """
        Get the prompter for the follower agent.
        :param is_visual: The flag indicating whether the agent is visual or not.
        :param main_prompt: The main prompt file path.
        :param example_prompt: The example prompt file path.
        :param api_prompt: The API prompt file path.
        :param app_info_prompt: The app information prompt file path.
        :param app_root_name: The root name of the app.
        :return: The prompter instance.
        """
        return FollowerAgentPrompter(
            is_visual,
            main_prompt,
            example_prompt,
            api_prompt,
            app_info_prompt,
            app_root_name,
        )

    def message_constructor(
        self,
        dynamic_examples: str,
        dynamic_tips: str,
        dynamic_knowledge: str,
        image_list: List,
        request_history: str,
        action_history: str,
        control_info: str,
        plan: List[str],
        request: str,
        current_state: dict,
        state_diff: dict,
        include_last_screenshot: bool,
    ) -> list:
        """
        Construct the prompt message for the FollowAgent.
        :param dynamic_examples: The dynamic examples retrieved from the self-demonstration and human demonstration.
        :param dynamic_tips: The dynamic tips retrieved from the self-demonstration and human demonstration.
        :param image_list: The list of screenshot images.
        :param request_history: The request history.
        :param action_history: The action history.
        :param plan: The plan.
        :param request: The request.
        :return: The prompt message.
        """
        followagent_prompt_system_message = self.prompter.system_prompt_construction(
            dynamic_examples, dynamic_tips
        )
        followagent_prompt_user_message = self.prompter.user_content_construction(
            image_list,
            request_history,
            action_history,
            control_info,
            plan,
            request,
            dynamic_knowledge,
            current_state,
            state_diff,
            include_last_screenshot,
        )

        followagent_prompt_message = self.prompter.prompt_construction(
            followagent_prompt_system_message, followagent_prompt_user_message
        )

        return followagent_prompt_message