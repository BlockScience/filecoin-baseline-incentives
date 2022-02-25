import streamlit as st


def glossary():
    st.write(
        """
## Glossary

### Raw Bytes Network Power (RB PiB)

Total network storage capacity. This is the sum of the total active onboarded storage by all miners and sectors.

### Block Reward

In a given period, the Block Reward is the sum total amount of Filecoin minted through Simple Minting and Baseline Minting mechanisms.

#### Simple Minting

A mechanism for issuing Filecoin as storage mining rewards through a function that decays exponentially with time.

#### Baseline Minting

Similiar to Simple Minting, but uses the concept of an "Effective Network Time," rather than the time since launch, for issuing rewards.

#### Effective Network Time (ENT)

A time-like measurement that captures, in effect, how the RB Network Power function tracks the Baseline Function. When RB Network Power is above the Baseline, ENT *tends* to move forward at the same rate as "real" time. Else, it *tends* to go slower. [1]

### Marginal Reward (MR)

Defined as the instantaneous Block Reward divided by the instantaneous RB Network Power. Indicates how much Filecoin is earned for a given unit of onboarded raw storage.

Marginal Reward Per Storage: $\omega(t) = \frac{BR(t)}{P_{rb}(t)}$

### Mining Utility (MU)

In order to make Marginal Reward comparisons relevant, it is important to contextualize these comparisons with respect to a common scenario. Mining Utility divides the Marginal Reward of any scenario against that common scenario—defined as the situation in which the RB Network Power is equal to the Baseline Function at every point in time (past, present and future).

Normalized Marginal Reward Per Power: $\pi(t) = \frac{\omega_s(t)}{\omega_b(t)}$

## References

[1]: Baseline Minting Incentives (Danilo Lessa Bernardineli, Gabriel Lefundes, Burrrata, Jeff Emmett, Jessica Zartler and ZX Zhang). https://medium.com/block-science/baseline-minting-incentives-743b229b9b80

[2]:
    """
)