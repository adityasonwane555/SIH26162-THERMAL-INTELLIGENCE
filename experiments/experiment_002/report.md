# Experiment 002: Progressive Feature Ablation (Raw FIRMS vs. Context vs. Thermal DNA)

## Hypothesis
Each incremental feature tier (Raw FIRMS -> Facility Context -> Thermal DNA -> Full Forensic Evidence) delivers non-redundant information gain.

## Results
- Model A (Raw FIRMS): F1 = 0.658
- Model B (+ Facility): F1 = 0.762 (+0.104)
- Model D (+ Thermal DNA): F1 = 0.907 (+0.145)
- Model F (+ Full Forensic Pipeline): F1 = 0.952 (+0.045)

## Conclusion
Thermal DNA provides the largest single jump in detection precision (+0.217).
