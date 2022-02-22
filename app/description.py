import streamlit as st


def description():
    st.write(
    """
# Filecoin Baseline Minting Educational Calculator content

Welcome to the Filecoin Baseline Minting Educational Calculator! This app allows you to interactively understand how Baseline Minting works in terms of mining incentives and what happens when the Baseline Function is crossed up or down.

As we're going to see, having Baseline Minting enhances the long-term sustainability and of network power by saving part of the block rewardwhen it's below the Baseline Function. Those savings accomplishes two functions:
- Enhances security by avoid distributing an disproportionate share of the rewards if an significant share of the network went down temporarily.
- Improves sustanability by distributing those savings to future miners when the network recovers and have it's power close to the baseline again

## Simulations

In order to visualize such effects, we'll be simulating what would be the baseline reward under different scenarios and comparing them directly. Specifically, the metric "Mining Utility" captures how much percent of an advantage the miner is having compared to an scenario where the Network Power is always equal to the Baseline.

Specifically, we have four scenarios on this app. Two for the user (`user` and `user-baseline-deactivated`) and two fixed (`optimistic` and `baseline`). 

On the left sidebar, you will find several options for controlling how the `user` scenarios for the Filecoin Network Power should grow with time.

### Scenarios

#### User

The `user` scenarios have their default settings assigned to an hypothetical situation, where the network doesn't grow initially, starts to grow at the same rate of the baseline function after some time, and it has sudden acceleration some years from now, only to get steady again.

In order to directly compare the effect of having Baseline Minting turned on or off, we have an second `user` defined scenario which is `user-baseline-deactivated`, which is analogous to deploying an fictious FIP on the beginning of the simulation which says "Baseline Minting now behaves just like Simple Minting".

*Technical specifics: this is done by iteratively increasing the cummulative capped power by the baseline function rather than the network power.*

#### Optimistic

The `optimistic` scenario is an scenario where the Network Power always grows as 5% as larger than the Baseline Function. 

#### Baseline

The `baseline` scenario is an scenario where the Network Power is always equal to the Baseline Function.

## References

[1]: Baseline Minting Incentives (Danilo Lessa Bernardineli, Gabriel Lefundes, Burrrata, Jeff Emmett, Jessica Zartler, ZX Zhang): https://medium.com/block-science/baseline-minting-incentives-743b229b9b80

[2]: Filecoin Network Crosses Baseline Sustainability Target for First Time
 (Danilo Lessa Bernardineli, Gabriel Lefundes, Jamsheed Shorish, ZX Zhang, Michael Zargham): https://filecoin.io/blog/posts/filecoin-network-crosses-baseline-sustainability-target-for-first-time/

## Contributors

This calculator has been developed as part of the collaboration between BlockScience and Filecoin. We acknowledge the work of the following collaborators for making it come to life:

- Will Wolf (BlockScience, ML engineer)
- Danilo Lessa Bernardineli (BlockScience, Subject Matter Expert)
- Burrrata (BlockScience, Community Lead)
- Jamsheed Shorish (BlockScience, Scientist)
- ZX Zhang (Protocol Labs, Research Lead at CryptoEconLab)
- (Insert your name and role here)

    """
    )
