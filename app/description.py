import streamlit as st

# TODO: Re-factor this document to reflect that'we re doing an Consesus Pledge Model

def description():
    st.write(
        """
**Baseline Minting enhances the long-term sustainability** of the Network Power by witholding part of the block reward when it's below the Baseline Function. These savings:

- **Enhance security** by witholding rewards if a significant share of the network temporarily goes down.
- **Improve sustainability** by distributing these rewards to future miners when the network recovers.

## Simulations

In order to visualize this behavior, we simulate the baseline reward under different scenarios then compare them directly. Specifically, the "Mining Utility" metric captures the percentage advantage a miner has as compared to a scenario in which the Network Power is always equal to the Baseline.

This app displays four scenarios: two for the user (`user` and `user-baseline-deactivated`) and two fixed (`optimistic` and `baseline`).

The left sidebar has several options for controlling how the `user` scenarios for the Filecoin Network Power grow with time.

## Scenarios

#### User

The default settings for the `user` scenarios encapsulate the following behavior: the network doesn't grow initially, later grows at the same rate as the Baseline Function, suddenly accelerates several years thereafter, then stabilizes eventually.

In order to directly compare the effect of turning Baseline Minting on or off, we show a second `user` scenario—`user-baseline-deactivated`—analogous to deploying a fictious FIP in which "Baseline Minting behaves like Simple Minting".

*Technical specifics: this is done by iteratively increasing the cumulative capped power of the Baseline Function rather than the Network Power.*

#### Optimistic

In the `optimistic` scenario, the Network Power grows 5% faster than the Baseline Function.

#### Baseline

In the `baseline` scenario, the Network Power is always equal to the Baseline Function.

## References

[1]: Filecoin Baseline Incentives GitHub Repository: https://github.com/BlockScience/filecoin-baseline-incentives

[2]: Baseline Minting Incentives (Danilo Lessa Bernardineli, Gabriel Lefundes, Burrrata, Jeff Emmett, Jessica Zartler, ZX Zhang): https://medium.com/block-science/baseline-minting-incentives-743b229b9b80

[3]: Filecoin Network Crosses Baseline Sustainability Target for First Time
 (Danilo Lessa Bernardineli, Gabriel Lefundes, Jamsheed Shorish, ZX Zhang, Michael Zargham): https://filecoin.io/blog/posts/filecoin-network-crosses-baseline-sustainability-target-for-first-time/

## Contributors

This calculator has been developed as part of the ongoing collaboration between BlockScience and Filecoin. We acknowledge the work of the following contributors for making it come to life:

- Will Wolf (BlockScience, ML Engineer)
- Danilo Lessa Bernardineli (BlockScience, Subject Matter Expert)
- Burrrata (BlockScience, Community Lead)
- Jamsheed Shorish (BlockScience, Scientist)
- ZX Zhang (Protocol Labs, Research Lead at CryptoEconLab)
    """
    )
