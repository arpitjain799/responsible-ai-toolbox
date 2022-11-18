// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

export interface IFeatureMetaData {
  identity_feature_name?: string;
  datetime_features?: string[];
  categorical_features?: string[];
  dropped_features?: string[];
  forecasting_grains?: string[];
}
