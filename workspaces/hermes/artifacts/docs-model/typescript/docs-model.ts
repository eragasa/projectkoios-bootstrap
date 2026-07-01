export type DocKind =
  | 'collection'
  | 'architecture'
  | 'adr'
  | 'spec'
  | 'brief'
  | 'workflow'
  | 'runbook'
  | 'policy'
  | 'role'
  | 'decision'
  | 'handoff'
  | 'archive'
  | 'aar'
  | 'note';

export type Lifecycle = 'draft' | 'active' | 'paused' | 'archived' | 'superseded';

export type Authority = 'normative' | 'advisory' | 'historical';

export interface DocNode {
  name: string;
  path: string;
  kind: DocKind;
  lifecycle: Lifecycle;
  authority: Authority;
  description?: string;
  metadata?: Record<string, unknown>;
  children: DocNode[];
}
