CREATE VIEW dataset AS
SELECT
	T1.commitHash,
	T1.inMainBranch,
	T1.committerDate,
	T1.committerTimezone,
	MAX(T2.complexity) AS maxComplexity,
	AVG(T2.complexity) AS meanComplexity,
	SUM(T2.linesAdded) As totalLinesAdded,
	SUM(T2.linesRemoved) AS totalLinesRemoved,
	SUM(T2.nloc) AS totalNloc,
	MAX(T2.tokenCount) AS maxTokenCount,
	AVG(T2.tokenCount) AS meanTokenCount,
	COUNT(*) AS changedFiles,
	CASE WHEN
		T3.key IS NULL THEN 0
		ELSE 1
	END AS faultInducingBool
FROM
	GIT_COMMITS T1
	LEFT JOIN GIT_COMMITS_CHANGES T2 ON T1.commitHash = T2.commitHash
	LEFT JOIN SZZ_FAULT_INDUCING_COMMITS T3 ON T3.faultInducingCommitHash = T1.commitHash
WHERE
	T2.nloc IS NOT NULL
	AND T2.complexity IS NOT NULL
	AND T2.tokenCount IS NOT NULL
	AND T1.committerTimezone NOT IN ("-19080", "11880")
GROUP BY
	T1.commitHash 

