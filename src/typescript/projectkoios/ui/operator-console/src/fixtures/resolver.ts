import {
  agentStatuses,
  changeProposals,
  contentBodies,
  contentRefs,
  evidenceRefs,
  externalStatuses,
  validationResults
} from "../../fixtures/operator-console-fixture";
import type {
  ChangeProposal,
  ContentRef,
  DashboardReadModel,
  EvidenceRef,
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

  buildDashboardReadModel(): DashboardReadModel {
    const primaryProposal: ChangeProposal | undefined = changeProposals[0];
    if (primaryProposal === undefined) {
      throw new Error("Missing primary change proposal fixture");
    }
    return {
      agentStatuses,
      externalStatuses,
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
    return problems;
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
}
