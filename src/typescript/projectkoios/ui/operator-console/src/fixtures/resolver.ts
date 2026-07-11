import {
  agentInteractions,
  agentMessages,
  agentStatuses,
  agentThreads,
  changeProposals,
  contentBodies,
  contentRefs,
  evidenceRefs,
  externalStatuses,
  validationResults
} from "../../fixtures/operator-console-fixture";
import type {
  AgentInteraction,
  AgentMessage,
  AgentThread,
  ChangeProposal,
  ContentRef,
  DashboardReadModel,
  EvidenceRef,
  ResolvedAgentInteraction,
  ResolvedAgentThread,
  ResolvedChangeProposal,
  ResolvedContent,
  ValidationResult
} from "../contracts";

export class FixtureGraphResolver {
  resolveContent(contentRefId: string): ResolvedContent {
    const contentRef: ContentRef = this.findContentRef(contentRefId);
    const body: string | undefined = contentBodies[contentRef.id];
    if (body === undefined) {
      throw new Error(`Missing content body: ${contentRef.id}`);
    }
    return { ref: contentRef, body };
  }

  resolveChangeProposal(proposal: ChangeProposal): ResolvedChangeProposal {
    return {
      proposal,
      current: this.resolveContent(proposal.currentRefId),
      proposed: this.resolveContent(proposal.proposedRefId),
      evidence: proposal.evidenceRefIds.map((evidenceRefId: string) => this.findEvidenceRef(evidenceRefId)),
      validations: proposal.validationResultIds.map((validationResultId: string) =>
        this.findValidationResult(validationResultId)
      )
    };
  }

  resolveAgentThread(thread: AgentThread): ResolvedAgentThread {
    return {
      thread,
      interactions: thread.interactionIds.map((interactionId: string) => this.resolveAgentInteraction(interactionId)),
      evidence: thread.evidenceRefIds.map((evidenceRefId: string) => this.findEvidenceRef(evidenceRefId))
    };
  }

  buildDashboardReadModel(): DashboardReadModel {
    const primaryProposal: ChangeProposal | undefined = changeProposals[0];
    if (primaryProposal === undefined) {
      throw new Error("Missing primary change proposal fixture");
    }
    return {
      agentStatuses,
      externalStatuses,
      interactionThreads: agentThreads.map((thread: AgentThread) => this.resolveAgentThread(thread)),
      primaryProposal: this.resolveChangeProposal(primaryProposal)
    };
  }

  validateFixtureGraph(): readonly string[] {
    const problems: string[] = [];
    for (const proposal of changeProposals) {
      try {
        this.resolveChangeProposal(proposal);
      } catch (error: unknown) {
        problems.push(error instanceof Error ? error.message : String(error));
      }
    }
    for (const thread of agentThreads) {
      try {
        this.resolveAgentThread(thread);
      } catch (error: unknown) {
        problems.push(error instanceof Error ? error.message : String(error));
      }
    }
    return problems;
  }

  private resolveAgentInteraction(interactionId: string): ResolvedAgentInteraction {
    const interaction: AgentInteraction = this.findAgentInteraction(interactionId);
    const message: AgentMessage = this.findAgentMessage(interaction.messageId);
    if (message.threadId !== interaction.threadId) {
      throw new Error(`Interaction/message thread mismatch: ${interaction.id}`);
    }
    return {
      interaction,
      message,
      evidence: this.findEvidenceRef(interaction.evidenceRefId)
    };
  }

  private findContentRef(contentRefId: string): ContentRef {
    const contentRef: ContentRef | undefined = contentRefs.find(
      (candidate: ContentRef) => candidate.id === contentRefId
    );
    if (contentRef === undefined) {
      throw new Error(`Missing content ref: ${contentRefId}`);
    }
    return contentRef;
  }

  private findEvidenceRef(evidenceRefId: string): EvidenceRef {
    const evidenceRef: EvidenceRef | undefined = evidenceRefs.find(
      (candidate: EvidenceRef) => candidate.id === evidenceRefId
    );
    if (evidenceRef === undefined) {
      throw new Error(`Missing evidence ref: ${evidenceRefId}`);
    }
    return evidenceRef;
  }

  private findValidationResult(validationResultId: string): ValidationResult {
    const validationResult: ValidationResult | undefined = validationResults.find(
      (candidate: ValidationResult) => candidate.id === validationResultId
    );
    if (validationResult === undefined) {
      throw new Error(`Missing validation result: ${validationResultId}`);
    }
    return validationResult;
  }

  private findAgentMessage(messageId: string): AgentMessage {
    const message: AgentMessage | undefined = agentMessages.find((candidate: AgentMessage) => candidate.id === messageId);
    if (message === undefined) {
      throw new Error(`Missing agent message: ${messageId}`);
    }
    return message;
  }

  private findAgentInteraction(interactionId: string): AgentInteraction {
    const interaction: AgentInteraction | undefined = agentInteractions.find(
      (candidate: AgentInteraction) => candidate.id === interactionId
    );
    if (interaction === undefined) {
      throw new Error(`Missing agent interaction: ${interactionId}`);
    }
    return interaction;
  }
}
