class TupleOut:

    @staticmethod
    def armor(str):
        return '({})'.format(str)

    @staticmethod
    def joint(tpl, armored=True):
        if type(tpl) is tuple:
            frags = []
            for t in tpl:
                frags.append(TupleOut.joint(t))
            result = ' '.join(frags)
            return TupleOut.armor(result) if armored else result
        else:
            return '{}'.format(tpl)