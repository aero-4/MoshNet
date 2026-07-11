export type BadStatus = {
    source: string;
    category?: string | null;
    result?: string | null;
};

export type DomainInfo = {
    domain_org?: string | null;
    created_at?: string | null;
    updated_at?: string | null;
    registrar?: Record<string, unknown> | null;
    registrant?: Record<string, unknown> | null;
    last_analysis_stats?: Record<string, number> | null;
    bad_statuses?: BadStatus[];
};

export type SiteInfo = {
    available?: boolean;
    url?: string;
    error?: string;
    title?: string | null;
    description?: string | null;
    links?: {
        total?: number;
        internal?: number;
        external?: number;
        sample?: string[];
    };
    forms?: {
        total?: number;
        password_fields?: number;
        external_actions?: string[];
    };
    suspicious_signals?: string[];
};

export type AnalyzeResult = {
    risk_score: number
    whois?: DomainInfo;
    virustotal?: DomainInfo;
    site?: SiteInfo;
};

export type SafetyState = "safe" | "danger" | "unknown";
