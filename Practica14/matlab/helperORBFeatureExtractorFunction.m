function [features, featureMetrics]= helperORBFeatureExtractorFunction(I)
% helperORBFeatureExtractorFunction Implements the ORB feature extraction 
% used in bagOfFeatures.
%
%   This is an example helper function that is subject to change or removal 
%   in future releases.

%   Copyright 2021 The MathWorks, Inc.

numPoints   = 1000;

% Detect ORB features
Igray  = im2gray(I);

points = detectORBFeatures(Igray, 'ScaleFactor', 1.2, 'NumLevels', 8);

% Select a subset of features, uniformly distributed throughout the image
points = selectUniform(points, numPoints, size(Igray, 1:2));

% Extract features
features = extractFeatures(Igray, points);

% Compute the Feature Metric. Use the variance of features as the metric
featureMetrics = var(single(features.Features),[],2);

