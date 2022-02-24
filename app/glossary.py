import streamlit as st


def glossary():
    st.write(
        """
## Glossary

### Raw Bytes Network Power (RB PiB)

How much storage capacity there is on the network. This is the sum of the total active onboarded storage by all miners and sectors.

### Block Reward

The Block Reward on a given period is the sum of how much Filecoin was minted through the Simple Minting and the Baseline Minting mechanisms.

#### Simple Minting

An mechanism for issuing Filecoin as storage mining rewards through an time exponentially decaying function.

#### Baseline Minting

Similiar to Simple Minting, but it uses the concept of an "Effective Network Time" rather than the time since launch for issuing rewards.

#### Effective Network Time (ENT)

An time-like measurement that takes into consideration how the RB Network Power historical trajectory is sucessful at tracking the Baseline Function. When RB Network Power is above the Baseline, then ENT *tends* to move forward with the same rate as the real time. Else, it *tends* to go slower than it. [1]

### Marginal Reward (MR)

An indicator about how much Filecoin is earned for any unit of onboarded raw storage. It is defined as the instantaneous block reward divided by the instantaneous RB network power.

Marginal Reward Per Storage: $\omega(t) = \frac{BR(t)}{P_{rb}(t)}$

### Mining Utility (MU)

In order to make Marginal Reward comparisons relevant, it is important to contextualize it in regards to an common scenario. Mining Utility divides the Marginal Reward of any scenario against that common scenario, which is defined as being the situation where the RB Network Power is equal to the Baseline Function at every point on time (past, present and future).

Normalized Marginal Reward Per Power: $\pi(t) = \frac{\omega_s(t)}{\omega_b(t)}$

## References

[1]: Baseline Minting Incentives (Danilo Lessa Bernardineli, Gabriel Lefundes, Burrrata, Jeff Emmett, Jessica Zartler and ZX Zhang). https://medium.com/block-science/baseline-minting-incentives-743b229b9b80

[2]: 
    """
    )

