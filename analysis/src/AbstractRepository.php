<?php
/**
 * Copyright (c) 2012-2019, Yegor Bugayenko
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met: 1) Redistributions of source code must retain the above
 * copyright notice, this list of conditions and the following
 * disclaimer. 2) Redistributions in binary form must reproduce the above
 * copyright notice, this list of conditions and the following
 * disclaimer in the documentation and/or other materials provided
 * with the distribution. 3) Neither the name of Yegor Bugayenko nor
 * the names of other contributors may be used to endorse or promote
 * products derived from this software without specific prior written
 * permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT
 * NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
 * FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
 * THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 * INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
 * STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
 * OF THE POSSIBILITY OF SUCH DAMAGE.
 */

require_once __DIR__ . '/Loc.php';
require_once __DIR__ . '/Repository.php';
require_once __DIR__ . '/Scv.php';

/**
 * Base repository.
 * @author Yegor Bugayenko <yegor@tpc2.com>
 */
abstract class AbstractRepository implements Repository
{
    /**
     * Name of the repo.
     */
    private $_name;
    /**
     * Public ctor.
     * @param string $name Name of the repo
     */
    protected function __construct($name)
    {
        $this->_name = $name;
    }
    /**
     * Make a repository by type, name, and URL.
     * @param string $type Type of it
     * @param string $name Name of the repo
     * @param string $url URL
     * @return Repository The repository just created
     */
    public static function factory($type, $name, $url)
    {
        if ($type == 'svn') {
            require_once __DIR__ . '/SvnRepository.php';
            $repo = new SvnRepository($name, $url);
        } elseif ($type == 'git') {
            require_once __DIR__ . '/GitRepository.php';
            $repo = new GitRepository($name, $url);
        } elseif ($type == 'hg') {
            require_once __DIR__ . '/HgRepository.php';
            $repo = new HgRepository($name, $url);
        } else {
            throw new Exception('unknown SCM type');
        }
        return $repo;
    }
    /**
     * Make it string.
     * @return string The text
     */
    public function __toString()
    {
        return $this->_name;
    }
    /**
     * Unique name of it.
     * @return string Name of it
     */
    public function name()
    {
        return $this->_name;
    }
    /**
     * Get lines of code metric from this repo.
     * @return Loc Lines of Java code, total
     */
    public function loc()
    {
        return new Loc($this);
    }
}
