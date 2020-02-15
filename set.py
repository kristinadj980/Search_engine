class SetItem:
    def __init__(self):
        self.document_path = None
        self.words_count = 0
        self.parents_count = 0
        self.parent_words_count = 0
        self.rank = 0

class Set:
    def __init__(self):
        self.items = []


    def union(self, sets):
        result = []

        if len(sets) == 1:
            return sets[0]

        for paths_set in sets:
            for path in paths_set:
                if path not in result:
                    result.append(path)

        return result

    def cross_section(self, sets):
        result = []
        union = self.union(sets)

        if len(sets) == 1:
            return sets[0]

        for path in union:
            is_cross_section = True
            for single_set in sets:
                if path not in single_set:
                    is_cross_section = False

            if is_cross_section:
                result.append(path)

        return result

    def complement(self, sets):
        union = self.union(sets)
        cross_section = self.cross_section(sets)

        if len(sets) == 1:
            return result

        for path in cross_section:
            if path in union:
                union.remove(path)

        return union