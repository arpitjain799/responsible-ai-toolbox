# Copyright (c) Microsoft Corporation
# Licensed under the MIT License.

import warnings
from typing import Any, Dict, List, Optional

from responsibleai.exceptions import UserConfigValidationException


class FeatureMetadata:
    def __init__(self,
                 identity_feature_name: Optional[str] = None,
                 time_column_name: Optional[str] = None,
                 categorical_features: Optional[List[str]] = None,
                 dropped_features: Optional[List[str]] = None):
        """Placeholder class for feature metadata provided by the user.

        :param identity_feature_name: Name of the feature which helps to
                                      uniquely identify a row or instance
                                      in user input dataset.
        :type identity_feature_name: Optional[str]
        :param datetime_features: List of datetime features in the
                                  user input dataset.
        :type datetime_features: Optional[List[str]]
        :param categorical_features: List of categorical features in the
                                     user input dataset.
        :type categorical_features: Optional[List[str]]
        :param dropped_features: List of features that were dropped by the
                                 the user during training of their model.
        :type dropped_features: Optional[List[str]]
        """
        self.identity_feature_name = identity_feature_name
        self.time_column_name = time_column_name
        self.categorical_features = categorical_features
        self.dropped_features = dropped_features
        self.time_series_id_column_names = time_series_id_column_names

        if self.categorical_features is not None:
            warnings.warn('categorical_features are not in use currently.')

    def validate(self, feature_names: List[str]):
        """Validate the user-provided feature metadata.
        
        :param feature_names: list of features in the dataset.
        :type feature_names: List[str]
        """
        self._validate_columns(
            'dropped feature', self.dropped_features, feature_names)
        self._validate_columns(
            'categorical feature', self.categorical_features, feature_names)
        self._validate_columns(
            'identity feature', self.identity_feature_name, feature_names)
        self._validate_columns(
            'time column', self.time_column_name, feature_names)
        self._validate_columns(
            'time series ID column',
            self.time_series_id_column_names,
            feature_names)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the feature metadata to a dictionary.

        :return: Dictionary of feature metadata.
        :rtype: Dict[str, Any]
        """
        return {
            'identity_feature_name': self.identity_feature_name,
            'datetime_features': self.datetime_features,
            'categorical_features': self.categorical_features,
            'dropped_features': self.dropped_features
        }

    def __eq__(self, other_feature_metadata) -> bool:
        """Compare the feature metadata with another feature metadata.

        :param other_feature_metadata: Feature metadata to compare with.
        :type other_feature_metadata: FeatureMetadata
        :return: True if the feature metadata is equal to the other feature
                 metadata.
        :rtype: bool
        """
        return self.identity_feature_name == \
            other_feature_metadata.identity_feature_name and \
            self.datetime_features == \
            other_feature_metadata.datetime_features and \
            self.categorical_features == \
            other_feature_metadata.categorical_features and \
            self.dropped_features == \
            other_feature_metadata.dropped_features and \
            self.time_series_id_column_names == \
            other_feature_metadata.time_series_id_column_names

    @staticmethod
    def _validate_columns(
            column_purpose: str,
            column_names: List[str],
            feature_names: List[str]):
        """Ensure the provided column is present in the dataset.

        :param column_purpose: The purpose the column fulfills in the dataset.
        :type column_purpose: str
        :param column_names: List of column names to validate.
        :type column_names: List[str]
        :param self.identity_feature_name: List of features in the user input dataset.
        :type self.identity_feature_name: List[str]
        """
        for column_name in column_names:
            if column_name not in feature_names:
                raise UserConfigValidationException(
                    f'The given {column_purpose} '
                    f'{column_name} is not present '
                    f'in the provided features: {", ".join(feature_names)}.')
